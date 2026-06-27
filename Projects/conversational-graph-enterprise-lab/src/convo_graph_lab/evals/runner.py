"""Conversation graph evaluation suite."""

from __future__ import annotations

import json
from pathlib import Path

from convo_graph_lab.config import Settings, get_settings
from convo_graph_lab.graph_engine.compiler import compile_graph
from convo_graph_lab.graph_engine.runner import GraphRunner
from convo_graph_lab.schema.models import EvalCase, EvalReport, EvalResult


def load_eval_cases(path: Path) -> list[EvalCase]:
    return [EvalCase(**item) for item in json.loads(path.read_text(encoding="utf-8"))]


def run_evaluations(settings: Settings | None = None) -> EvalReport:
    settings = settings or get_settings()
    graph, issues = compile_graph(settings.data_dir / "sample_graphs" / "enterprise_orchestrator.json")
    if any(issue.severity == "error" for issue in issues):
        raise RuntimeError(f"Graph has compiler errors: {issues}")
    cases = load_eval_cases(settings.data_dir / "eval_cases" / "conversation_eval_cases.json")
    results: list[EvalResult] = []
    for case in cases:
        runner = GraphRunner(graph, settings=settings)
        result = runner.start(case.inputs[0], user_id="eval-user", session_id=case.id)
        for followup in case.inputs[1:]:
            result = runner.send_input(case.id, followup)
        path_ok = all(node_id in result.path for node_id in case.expected_path_contains)
        slots_ok = all(result.state.context.slots.get(key) == value for key, value in case.expected_slots.items())
        score = (0.5 if path_ok else 0.0) + (0.5 if slots_ok else 0.0)
        results.append(EvalResult(case_id=case.id, passed=path_ok and slots_ok, score=score, details=f"path={result.path} slots={result.state.context.slots}"))
    pass_rate = sum(1 for result in results if result.passed) / max(len(results), 1)
    report = EvalReport(suite="conversation_graph", results=results, pass_rate=round(pass_rate, 3))
    settings.export_dir.mkdir(parents=True, exist_ok=True)
    (settings.export_dir / "evaluation_report.json").write_text(report.model_dump_json(indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    print(run_evaluations().model_dump_json(indent=2))
