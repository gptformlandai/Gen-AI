from __future__ import annotations

import json
from pathlib import Path

from enterprise_ops_lab.runner import EnterpriseOpsRunner
from enterprise_ops_lab.schemas.evaluation import EvaluationReport, EvaluationRow
from enterprise_ops_lab.schemas.incident import IncidentRequest


def run_trajectory_eval(path: Path) -> EvaluationReport:
    cases = json.loads(path.read_text(encoding="utf-8"))
    runner = EnterpriseOpsRunner()
    rows: list[EvaluationRow] = []
    for case in cases:
        response = runner.run(IncidentRequest(query=case["query"], session_id=f"trajectory-{case['id']}"))
        trajectory = response.tool_trajectory
        checks = {
            "must_include": set(case["must_include"]).issubset(set(trajectory)),
            "must_call_before": all(index_of(trajectory, before) < index_of(trajectory, after) for before, after in case["must_call_before"]),
        }
        rows.append(EvaluationRow(case_id=case["id"], passed=all(checks.values()), checks=checks))
    passed = sum(row.passed for row in rows)
    return EvaluationReport(name="trajectory", total=len(rows), passed=passed, pass_rate=passed / max(len(rows), 1), rows=rows)


def index_of(values: list[str], target: str) -> int:
    return values.index(target) if target in values else 10_000

