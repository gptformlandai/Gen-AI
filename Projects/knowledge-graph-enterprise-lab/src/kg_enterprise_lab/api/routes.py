"""FastAPI route registration."""

from __future__ import annotations

from kg_enterprise_lab.algorithms.blast_radius import blast_radius
from kg_enterprise_lab.evaluation.evaluation_runner import run_all_evaluations
from kg_enterprise_lab.extraction.rule_based_extractor import RuleBasedExtractor
from kg_enterprise_lab.graph.graph_analysis import summarize_graph
from kg_enterprise_lab.graphrag.graphrag_pipeline import GraphRAGPipeline
from kg_enterprise_lab.ingestion.ingestion_pipeline import build_ingestion_report, load_documents
from kg_enterprise_lab.ontology.ontology_models import default_ontology
from kg_enterprise_lab.ontology.ontology_validator import OntologyValidator
from kg_enterprise_lab.query.graph_query_service import GraphQueryService
from kg_enterprise_lab.query.sparql_executor import execute_sparql_template
from kg_enterprise_lab.resolution.entity_resolver import EntityResolver
from kg_enterprise_lab.schemas.graphrag import GraphRAGRequest
from kg_enterprise_lab.schemas.query import QueryRequest
from kg_enterprise_lab.visualization.visualization_service import VisualizationService


def register_routes(app, get_graph_dependency) -> None:
    from fastapi import Depends, HTTPException

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/ingest")
    def ingest() -> dict[str, object]:
        return build_ingestion_report().model_dump()

    @app.post("/extract/entities")
    def extract_entities(graph=Depends(get_graph_dependency)) -> dict[str, object]:
        document = load_documents()[0]
        batch = RuleBasedExtractor(graph).extract(document)
        return {"entities": [item.model_dump() for item in batch.entities]}

    @app.post("/extract/relationships")
    def extract_relationships(graph=Depends(get_graph_dependency)) -> dict[str, object]:
        document = load_documents()[0]
        batch = RuleBasedExtractor(graph).extract(document)
        return {"relationships": [item.model_dump() for item in batch.relationships]}

    @app.post("/graph/query")
    def graph_query(request: QueryRequest, graph=Depends(get_graph_dependency)):
        return GraphQueryService(graph).answer(request).model_dump()

    @app.get("/graph/summary")
    def graph_summary(graph=Depends(get_graph_dependency)):
        return summarize_graph(graph).model_dump()

    @app.get("/graph/sparql/{template}")
    def graph_sparql(template: str, graph=Depends(get_graph_dependency)):
        return {"template": template, "rows": execute_sparql_template(graph, template)}

    @app.post("/graph/graphrag")
    def graph_graphrag(request: GraphRAGRequest, graph=Depends(get_graph_dependency)):
        return GraphRAGPipeline(graph).run(request).model_dump()

    @app.get("/graph/node/{node_id}")
    def get_node(node_id: str, graph=Depends(get_graph_dependency)):
        node = graph.get_node(node_id)
        if not node:
            raise HTTPException(status_code=404, detail="node not found")
        return node.model_dump()

    @app.get("/graph/neighbors/{node_id}")
    def get_neighbors(node_id: str, graph=Depends(get_graph_dependency)):
        return [node.model_dump() for node in graph.neighbors(node_id)]

    @app.get("/graph/path")
    def get_path(source: str, target: str, graph=Depends(get_graph_dependency)):
        resolver = EntityResolver(graph)
        source_id = resolver.resolve_name(source)
        target_id = resolver.resolve_name(target)
        if not source_id or not target_id:
            raise HTTPException(status_code=404, detail="source or target not found")
        path, rels = graph.shortest_path(source_id, target_id)
        return {"node_ids": path, "relationship_ids": rels}

    @app.get("/graph/blast-radius/{service}")
    def get_blast_radius(service: str, graph=Depends(get_graph_dependency)):
        resolver = EntityResolver(graph)
        node_id = resolver.resolve_name(service)
        if not node_id:
            raise HTTPException(status_code=404, detail="service not found")
        nodes, rels = blast_radius(graph, node_id)
        return {"node_ids": sorted(nodes), "relationship_ids": sorted(rels)}

    @app.get("/graph/lineage/{service}")
    def get_lineage(service: str, graph=Depends(get_graph_dependency)):
        resolver = EntityResolver(graph)
        node_id = resolver.resolve_name(service)
        if not node_id:
            raise HTTPException(status_code=404, detail="service not found")
        nodes, rels = graph.traverse(node_id, "out", {"HAS_LINEAGE_TO", "CALLS", "READS_FROM", "WRITES_TO"}, 4)
        return {"node_ids": sorted(nodes), "relationship_ids": sorted(rels)}

    @app.get("/graph/visualize/{view}")
    def visualize(view: str, fmt: str = "json", anchor: str | None = None, graph=Depends(get_graph_dependency)):
        return VisualizationService(graph).export(fmt=fmt, view=view, anchor_name=anchor)

    @app.post("/graph/validate")
    def validate_graph(graph=Depends(get_graph_dependency)):
        issues = OntologyValidator(default_ontology()).validate_graph(graph)
        return {"issues": [issue.model_dump() for issue in issues]}

    @app.post("/eval/run")
    def run_eval():
        return [report.model_dump() for report in run_all_evaluations()]
