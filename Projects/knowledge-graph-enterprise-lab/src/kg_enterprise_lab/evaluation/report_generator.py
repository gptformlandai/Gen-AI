"""Evaluation report generation."""

from __future__ import annotations

from kg_enterprise_lab.schemas.evaluation import EvalReport, EvalResult


def make_report(suite: str, results: list[EvalResult]) -> EvalReport:
    pass_rate = sum(1 for result in results if result.passed) / max(len(results), 1)
    return EvalReport(suite=suite, results=results, pass_rate=round(pass_rate, 3))


def report_to_markdown(reports: list[EvalReport]) -> str:
    lines = ["# Evaluation Report", ""]
    for report in reports:
        lines.append(f"## {report.suite}")
        lines.append("")
        lines.append(f"Pass rate: {report.pass_rate}")
        lines.append("")
        for result in report.results:
            status = "PASS" if result.passed else "FAIL"
            lines.append(f"- {status} `{result.case_id}` score={result.score}: {result.details}")
        lines.append("")
    return "\n".join(lines)
