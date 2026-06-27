"""Run all local evaluation suites."""

from __future__ import annotations

import json
from pathlib import Path

from kg_enterprise_lab.config import Settings, get_settings
from kg_enterprise_lab.evaluation.entity_eval import evaluate_entity_extraction
from kg_enterprise_lab.evaluation.graph_quality_eval import evaluate_graph_quality
from kg_enterprise_lab.evaluation.graphrag_eval import evaluate_graphrag
from kg_enterprise_lab.evaluation.query_eval import evaluate_queries
from kg_enterprise_lab.evaluation.relationship_eval import evaluate_relationship_extraction
from kg_enterprise_lab.evaluation.report_generator import make_report, report_to_markdown
from kg_enterprise_lab.ingestion.ingestion_pipeline import build_sample_graph
from kg_enterprise_lab.schemas.evaluation import EvalCase, EvalReport


def _load_cases(path: Path) -> list[EvalCase]:
    return [EvalCase(**item) for item in json.loads(path.read_text(encoding="utf-8"))]


def run_all_evaluations(settings: Settings | None = None) -> list[EvalReport]:
    settings = settings or get_settings()
    graph = build_sample_graph(settings)
    eval_dir = settings.data_dir / "eval"
    reports = [
        make_report("entity_extraction", evaluate_entity_extraction(graph, _load_cases(eval_dir / "entity_extraction_cases.json"))),
        make_report("relationship_extraction", evaluate_relationship_extraction(graph, _load_cases(eval_dir / "relationship_extraction_cases.json"))),
        make_report("query", evaluate_queries(graph, _load_cases(eval_dir / "query_cases.json"))),
        make_report("graphrag", evaluate_graphrag(graph, _load_cases(eval_dir / "graphrag_cases.json"))),
        make_report("graph_quality", evaluate_graph_quality(graph)),
    ]
    settings.export_dir.mkdir(parents=True, exist_ok=True)
    (settings.export_dir / "evaluation_report.md").write_text(report_to_markdown(reports), encoding="utf-8")
    return reports


if __name__ == "__main__":
    for report in run_all_evaluations():
        print(f"{report.suite}: {report.pass_rate}")
