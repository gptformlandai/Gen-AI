"""Allowlisted local SPARQL-style executor.

This is not a full SPARQL engine. It intentionally executes only the templates
in ``sparql_templates.py`` against the local triple store so RDF examples remain
runnable without a server. Production deployments should send the same
allowlisted templates to a real SPARQL endpoint.
"""

from __future__ import annotations

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository
from kg_enterprise_lab.ontology.rdf_serializer import graph_to_triples
from kg_enterprise_lab.query.sparql_templates import get_sparql_template


TEMPLATE_PREDICATES = {
    "service_dependencies": "DEPENDS_ON",
    "service_owners": "OWNED_BY",
    "incident_runbooks": "DOCUMENTED_BY",
    "lineage": "HAS_LINEAGE_TO",
}


def execute_sparql_template(graph: InMemoryGraphRepository, template_name: str) -> list[dict[str, str]]:
    get_sparql_template(template_name)
    if template_name not in TEMPLATE_PREDICATES:
        raise ValueError(f"No local executor is registered for SPARQL template: {template_name}")
    predicate = TEMPLATE_PREDICATES[template_name]
    triples = graph_to_triples(graph).query_predicate(predicate)
    left_key, right_key = _keys_for_template(template_name)
    return [
        {left_key: subject, right_key: obj, "predicate": predicate}
        for subject, _, obj in triples
    ]


def _keys_for_template(template_name: str) -> tuple[str, str]:
    if template_name == "service_owners":
        return "service", "team"
    if template_name == "incident_runbooks":
        return "incident", "runbook"
    if template_name == "lineage":
        return "source", "target"
    return "service", "dependency"
