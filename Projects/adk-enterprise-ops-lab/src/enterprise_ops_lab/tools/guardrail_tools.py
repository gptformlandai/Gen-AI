from __future__ import annotations

from enterprise_ops_lab.guardrails.input_guardrails import check_input
from enterprise_ops_lab.guardrails.output_guardrails import validate_output
from enterprise_ops_lab.guardrails.redaction import redact_sensitive_data
from enterprise_ops_lab.guardrails.tool_guardrails import validate_tool_call


def input_check(query: str) -> dict:
    ok, reason = check_input(query)
    return {"ok": ok, "reason": reason, "redacted_query": redact_sensitive_data(query)}


def output_check(text: str, confidence: float) -> dict:
    ok, reason = validate_output(text, confidence)
    return {"ok": ok, "reason": reason, "redacted_output": redact_sensitive_data(text)}


def tool_call_check(tool_name: str, approved: bool = False) -> dict:
    ok, reason = validate_tool_call(tool_name, approved=approved)
    return {"ok": ok, "reason": reason}

