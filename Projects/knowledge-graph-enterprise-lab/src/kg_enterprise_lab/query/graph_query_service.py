"""High-level graph question answering service."""

from __future__ import annotations

from kg_enterprise_lab.algorithms.blast_radius import blast_radius, impacted_owners
from kg_enterprise_lab.algorithms.centrality import highest_dependency_centrality
from kg_enterprise_lab.governance.query_policy import is_allowed_intent
from kg_enterprise_lab.governance.risk_checker import check_traversal_depth
from kg_enterprise_lab.ontology.ontology_models import default_ontology
from kg_enterprise_lab.ontology.ontology_validator import OntologyValidator
from kg_enterprise_lab.query.query_explainer import explain_plan
from kg_enterprise_lab.resolution.duplicate_detector import detect_duplicates
from kg_enterprise_lab.resolution.entity_resolver import EntityResolver
from kg_enterprise_lab.schemas.query import PathResult, QueryPlan, QueryRequest, QueryResponse


class GraphQueryService:
    def __init__(self, graph) -> None:
        self.graph = graph
        self.resolver = EntityResolver(graph)

    def answer(self, request: QueryRequest, plan: QueryPlan | None = None) -> QueryResponse:
        from kg_enterprise_lab.query.query_planner import plan_query

        plan = plan or plan_query(request)
        if not is_allowed_intent(plan.intent):
            return QueryResponse(question=request.question, intent=plan.intent, answer=f"Intent is not allowlisted: {plan.intent}", confidence=0.0)
        risk_notes = check_traversal_depth(request.max_depth)
        if risk_notes:
            return QueryResponse(question=request.question, intent=plan.intent, answer="Query rejected by traversal policy: " + "; ".join(risk_notes), explanation=risk_notes, confidence=0.0)
        handlers = {
            "dependents": self._dependents,
            "blast_radius": self._blast_radius,
            "shortest_path": self._shortest_path,
            "ownership": self._ownership,
            "similar_incidents": self._similar_incidents,
            "runbook_search": self._runbook_search,
            "lineage": self._lineage,
            "centrality": self._centrality,
            "validate": self._validate,
            "duplicates": self._duplicates,
            "rdf_compare": self._rdf_compare,
            "generic": self._generic,
        }
        response = handlers.get(plan.intent, self._generic)(request, plan)
        if request.include_explanation:
            response.explanation = explain_plan(plan) + response.explanation
        return response

    def _resolve(self, name: str | None) -> str | None:
        if not name:
            return None
        return self.resolver.resolve_name(name)

    def _dependents(self, request: QueryRequest, plan: QueryPlan) -> QueryResponse:
        node_id = self._resolve(plan.entity_name)
        if not node_id:
            return self._not_found(request, plan)
        rels = self.graph.relationships_for_node(node_id, "in", {"DEPENDS_ON", "CALLS"})
        services = list({rel.source_id: self.graph.get_node(rel.source_id) for rel in rels if self.graph.get_node(rel.source_id)}.values())
        names = sorted(node.name for node in services)
        return QueryResponse(
            question=request.question,
            intent=plan.intent,
            answer=f"Services depending on {self.graph.get_node(node_id).name}: {', '.join(names) or 'none found'}.",
            node_ids=[node_id] + [node.id for node in services],
            relationship_ids=[rel.id for rel in rels],
            confidence=0.95,
        )

    def _blast_radius(self, request: QueryRequest, plan: QueryPlan) -> QueryResponse:
        node_id = self._resolve(plan.entity_name)
        if not node_id:
            return self._not_found(request, plan)
        node_ids, rel_ids = blast_radius(self.graph, node_id, request.max_depth)
        names = [self.graph.get_node(item).name for item in sorted(node_ids) if self.graph.get_node(item)]
        owners = impacted_owners(self.graph, node_ids)
        return QueryResponse(
            question=request.question,
            intent=plan.intent,
            answer=f"Blast radius includes {len(node_ids)} nodes: {', '.join(names)}. Contact: {', '.join(owners) or 'owner not found'}.",
            node_ids=sorted(node_ids),
            relationship_ids=sorted(rel_ids),
            confidence=0.9,
        )

    def _shortest_path(self, request: QueryRequest, plan: QueryPlan) -> QueryResponse:
        source_id = self._resolve(plan.entity_name)
        target_id = self._resolve(plan.target_name)
        if not source_id or not target_id:
            return self._not_found(request, plan)
        path, rel_path = self.graph.shortest_path(source_id, target_id, max_depth=request.max_depth + 2)
        names = [self.graph.get_node(node_id).name for node_id in path if self.graph.get_node(node_id)]
        return QueryResponse(
            question=request.question,
            intent=plan.intent,
            answer=" -> ".join(names) if names else "No path found.",
            node_ids=path,
            relationship_ids=rel_path,
            paths=[PathResult(node_ids=path, relationship_ids=rel_path)] if path else [],
            confidence=0.88 if path else 0.3,
        )

    def _ownership(self, request: QueryRequest, plan: QueryPlan) -> QueryResponse:
        node_id = self._resolve(plan.entity_name)
        if not node_id:
            return self._not_found(request, plan)
        node_ids, _ = blast_radius(self.graph, node_id, request.max_depth)
        owners = impacted_owners(self.graph, node_ids)
        return QueryResponse(
            question=request.question,
            intent=plan.intent,
            answer=f"Impacted owner/team contacts: {', '.join(owners) or 'none found'}.",
            node_ids=sorted(node_ids),
            confidence=0.85,
        )

    def _similar_incidents(self, request: QueryRequest, plan: QueryPlan) -> QueryResponse:
        node_id = self._resolve(plan.entity_name)
        if not node_id:
            return self._not_found(request, plan)
        base = self.graph.get_node(node_id)
        base_terms = set(str(base.properties.get("symptoms", [])).lower().split()) if base else set()
        scored: list[tuple[str, int]] = []
        for incident in self.graph.find_nodes(label="Incident"):
            if incident.id == node_id:
                continue
            terms = set(str(incident.properties.get("symptoms", [])).lower().split())
            overlap = len(base_terms & terms)
            if overlap:
                scored.append((incident.id, overlap))
        names = [self.graph.get_node(item[0]).name for item in sorted(scored, key=lambda item: item[1], reverse=True)]
        return QueryResponse(question=request.question, intent=plan.intent, answer=f"Similar incidents: {', '.join(names) or 'none found'}.", node_ids=[node_id] + [item[0] for item in scored])

    def _runbook_search(self, request: QueryRequest, plan: QueryPlan) -> QueryResponse:
        text = request.question.lower()
        matches = []
        for runbook in self.graph.find_nodes(label="Runbook"):
            haystack = runbook.searchable_text()
            if any(term in haystack for term in text.split() if len(term) > 3):
                matches.append(runbook)
        return QueryResponse(
            question=request.question,
            intent=plan.intent,
            answer=f"Matching runbooks: {', '.join(node.name for node in matches) or 'none found'}.",
            node_ids=[node.id for node in matches],
            confidence=0.82,
        )

    def _lineage(self, request: QueryRequest, plan: QueryPlan) -> QueryResponse:
        node_id = self._resolve(plan.entity_name) or self._resolve("mobile-app")
        node_ids, rel_ids = self.graph.traverse(node_id, "out", {"HAS_LINEAGE_TO", "CALLS", "READS_FROM", "WRITES_TO"}, request.max_depth)
        names = [self.graph.get_node(item).name for item in sorted(node_ids) if self.graph.get_node(item)]
        return QueryResponse(question=request.question, intent=plan.intent, answer=f"Lineage path touches: {', '.join(names)}.", node_ids=sorted(node_ids), relationship_ids=sorted(rel_ids), confidence=0.86)

    def _centrality(self, request: QueryRequest, plan: QueryPlan) -> QueryResponse:
        top = highest_dependency_centrality(self.graph)
        if not top:
            return self._not_found(request, plan)
        node = self.graph.get_node(top[0])
        return QueryResponse(question=request.question, intent=plan.intent, answer=f"{node.name} has the highest dependency centrality score: {top[1]}.", node_ids=[top[0]], confidence=0.87)

    def _validate(self, request: QueryRequest, plan: QueryPlan) -> QueryResponse:
        issues = OntologyValidator(default_ontology()).validate_graph(self.graph)
        errors = [issue for issue in issues if issue.severity == "error"]
        return QueryResponse(question=request.question, intent=plan.intent, answer=f"Validation found {len(errors)} errors and {len(issues) - len(errors)} warnings.", confidence=0.9)

    def _duplicates(self, request: QueryRequest, plan: QueryPlan) -> QueryResponse:
        duplicates = detect_duplicates(self.graph)
        answer = "; ".join(f"{left} ~ {right} ({score})" for left, right, score in duplicates) or "No duplicates found."
        return QueryResponse(question=request.question, intent=plan.intent, answer=answer, node_ids=[item for pair in duplicates for item in pair[:2]], confidence=0.84)

    def _rdf_compare(self, request: QueryRequest, plan: QueryPlan) -> QueryResponse:
        return QueryResponse(
            question=request.question,
            intent=plan.intent,
            answer="Property graph stores rich node/relationship properties and path traversals; RDF stores subject-predicate-object triples with URI semantics, OWL/RDFS vocabularies, and SPARQL querying.",
            confidence=0.9,
        )

    def _generic(self, request: QueryRequest, plan: QueryPlan) -> QueryResponse:
        return QueryResponse(question=request.question, intent=plan.intent, answer="I can answer dependency, ownership, lineage, centrality, duplicate, validation, RDF, and GraphRAG questions over the enterprise graph.", confidence=0.55)

    def _not_found(self, request: QueryRequest, plan: QueryPlan) -> QueryResponse:
        return QueryResponse(question=request.question, intent=plan.intent, answer="I could not link the requested entity to the graph.", confidence=0.2)
