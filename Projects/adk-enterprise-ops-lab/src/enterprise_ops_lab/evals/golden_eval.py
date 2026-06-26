from __future__ import annotations

import json
from pathlib import Path

from enterprise_ops_lab.runner import EnterpriseOpsRunner
from enterprise_ops_lab.schemas.evaluation import EvaluationReport, EvaluationRow
from enterprise_ops_lab.schemas.incident import IncidentRequest


def run_golden_eval(path: Path) -> EvaluationReport:
    cases = json.loads(path.read_text(encoding="utf-8"))
    runner = EnterpriseOpsRunner()
    rows: list[EvaluationRow] = []
    for case in cases:
        response = runner.run(IncidentRequest(query=case["query"], session_id=f"eval-{case['id']}"))
        checks = {
            "service": response.triage.service == case["expected_service"],
            "severity": response.triage.severity == case["expected_severity"],
            "required_tools": set(case["required_tools"]).issubset(set(response.tool_trajectory)),
            "required_terms": all(term.lower() in response.final_answer.lower() for term in case["required_terms"]),
        }
        rows.append(EvaluationRow(case_id=case["id"], passed=all(checks.values()), checks=checks))
    passed = sum(row.passed for row in rows)
    return EvaluationReport(name="golden", total=len(rows), passed=passed, pass_rate=passed / max(len(rows), 1), rows=rows)

