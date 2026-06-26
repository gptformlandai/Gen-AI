from __future__ import annotations

from enterprise_ops_lab.tools.evaluation_tools import evaluate_response_quality


def run(response: dict, required_terms: list[str] | None = None, required_tools: list[str] | None = None) -> dict:
    return evaluate_response_quality(response, required_terms=required_terms, required_tools=required_tools)

