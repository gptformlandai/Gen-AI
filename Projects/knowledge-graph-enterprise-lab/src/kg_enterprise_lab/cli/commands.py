"""CLI commands for the enterprise knowledge graph lab."""

from __future__ import annotations

import argparse
import json
import sys

from kg_enterprise_lab.algorithms.centrality import degree_centrality, highest_dependency_centrality
from kg_enterprise_lab.algorithms.connected_components import connected_components
from kg_enterprise_lab.algorithms.cycle_detection import detect_cycles
from kg_enterprise_lab.algorithms.pagerank import pagerank
from kg_enterprise_lab.algorithms.topological_sort import topological_sort
from kg_enterprise_lab.config import get_settings
from kg_enterprise_lab.evaluation.evaluation_runner import run_all_evaluations
from kg_enterprise_lab.graph.graph_analysis import summarize_graph
from kg_enterprise_lab.graphrag.graphrag_pipeline import GraphRAGPipeline
from kg_enterprise_lab.ingestion.ingestion_pipeline import build_ingestion_report, build_sample_graph
from kg_enterprise_lab.ontology.ontology_models import default_ontology
from kg_enterprise_lab.ontology.ontology_validator import OntologyValidator
from kg_enterprise_lab.ontology.rdf_serializer import graph_to_turtle
from kg_enterprise_lab.query.graph_query_service import GraphQueryService
from kg_enterprise_lab.query.sparql_executor import execute_sparql_template
from kg_enterprise_lab.resolution.duplicate_detector import detect_duplicates
from kg_enterprise_lab.schemas.graphrag import GraphRAGRequest
from kg_enterprise_lab.schemas.query import QueryRequest
from kg_enterprise_lab.visualization.visualization_service import VisualizationService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="kg-lab", description="Enterprise Knowledge Graph Lab CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("ingest-sample-data")
    sub.add_parser("build-graph")
    sub.add_parser("graph-summary")

    query = sub.add_parser("query-graph")
    query.add_argument("--question", required=True)

    sparql = sub.add_parser("run-sparql")
    sparql.add_argument("--template", default="service_dependencies")

    graphrag = sub.add_parser("run-graphrag")
    graphrag.add_argument("--question", required=True)

    export = sub.add_parser("export-graph")
    export.add_argument("--format", choices=["json", "mermaid", "dot", "ttl"], default="json")
    export.add_argument("--view", default="full")
    export.add_argument("--anchor", default=None)

    sub.add_parser("validate-ontology")
    sub.add_parser("detect-duplicates")
    sub.add_parser("run-algorithms")
    sub.add_parser("run-evals")
    sub.add_parser("start-api")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    settings = get_settings()
    graph = build_sample_graph(settings)

    if args.command == "ingest-sample-data":
        print(json.dumps(build_ingestion_report(settings).model_dump(), indent=2))
    elif args.command == "build-graph":
        graph.save_json(settings.graph_state_path)
        print(f"saved graph to {settings.graph_state_path}")
    elif args.command == "graph-summary":
        print(json.dumps(summarize_graph(graph).model_dump(), indent=2))
    elif args.command == "query-graph":
        response = GraphQueryService(graph).answer(QueryRequest(question=args.question))
        print(json.dumps(response.model_dump(), indent=2))
    elif args.command == "run-sparql":
        print(json.dumps(execute_sparql_template(graph, args.template), indent=2))
    elif args.command == "run-graphrag":
        response = GraphRAGPipeline(graph).run(GraphRAGRequest(question=args.question))
        print(json.dumps(response.model_dump(), indent=2))
    elif args.command == "export-graph":
        output = _export_graph(args, graph)
        print(output)
    elif args.command == "validate-ontology":
        issues = OntologyValidator(default_ontology()).validate_graph(graph)
        print(json.dumps([issue.model_dump() for issue in issues], indent=2))
    elif args.command == "detect-duplicates":
        print(json.dumps(detect_duplicates(graph), indent=2))
    elif args.command == "run-algorithms":
        payload = {
            "degree_centrality": degree_centrality(graph, "Service"),
            "highest_dependency_centrality": highest_dependency_centrality(graph),
            "pagerank": dict(list(pagerank(graph, {"DEPENDS_ON", "CALLS"}).items())[:10]),
            "connected_components": [sorted(component) for component in connected_components(graph)],
            "cycles": detect_cycles(graph),
            "topological_sort": topological_sort(graph),
        }
        print(json.dumps(payload, indent=2))
    elif args.command == "run-evals":
        reports = run_all_evaluations(settings)
        print(json.dumps([report.model_dump() for report in reports], indent=2))
    elif args.command == "start-api":
        return _start_api()
    return 0


def _export_graph(args: argparse.Namespace, graph) -> str:
    settings = get_settings()
    service = VisualizationService(graph)
    if args.format == "ttl":
        turtle = graph_to_turtle(graph)
        path = settings.export_dir / "enterprise_graph.ttl"
        path.write_text(turtle, encoding="utf-8")
        return turtle
    exported = service.export(fmt=args.format, view=args.view, anchor_name=args.anchor)
    suffix = {"json": "json", "mermaid": "md", "dot": "dot"}[args.format]
    path = settings.export_dir / f"graph_{args.view}.{suffix}"
    if isinstance(exported, dict):
        text = json.dumps(exported, indent=2)
    else:
        text = exported
    path.write_text(text, encoding="utf-8")
    return text


def _start_api() -> int:
    try:
        import uvicorn
    except ImportError:
        print("Install API dependencies first: python -m pip install -e '.[api]'", file=sys.stderr)
        return 2
    uvicorn.run("kg_enterprise_lab.api.app:app", host="127.0.0.1", port=8000, reload=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
