from __future__ import annotations


def evaluate_response_quality(response: dict, required_terms: list[str] | None = None, required_tools: list[str] | None = None) -> dict:
    final_answer = str(response.get("final_answer", "")).lower()
    trajectory = set(response.get("tool_trajectory", []))
    term_checks = {term: term.lower() in final_answer for term in required_terms or []}
    tool_checks = {tool: tool in trajectory for tool in required_tools or []}
    passed = all(term_checks.values()) and all(tool_checks.values())
    return {
        "passed": passed,
        "term_checks": term_checks,
        "tool_checks": tool_checks,
        "score": round((sum(term_checks.values()) + sum(tool_checks.values())) / max(len(term_checks) + len(tool_checks), 1), 2),
    }

