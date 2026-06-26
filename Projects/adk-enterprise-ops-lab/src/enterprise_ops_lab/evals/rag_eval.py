from __future__ import annotations

import json
from pathlib import Path

from enterprise_ops_lab.rag.retriever import RunbookRetriever
from enterprise_ops_lab.schemas.evaluation import EvaluationReport, EvaluationRow


def run_rag_eval(path: Path, runbook_dir: Path) -> EvaluationReport:
    cases = json.loads(path.read_text(encoding="utf-8"))
    retriever = RunbookRetriever(runbook_dir)
    rows: list[EvaluationRow] = []
    for case in cases:
        evidence = retriever.search(case["query"], k=3)
        joined = " ".join(item.quote for item in evidence).lower()
        checks = {
            "source": any(item.source == case["expected_source"] for item in evidence),
            "terms": all(term.lower() in joined for term in case["required_terms"]),
        }
        rows.append(EvaluationRow(case_id=case["id"], passed=all(checks.values()), checks=checks))
    passed = sum(row.passed for row in rows)
    return EvaluationReport(name="rag_grounding", total=len(rows), passed=passed, pass_rate=passed / max(len(rows), 1), rows=rows)

