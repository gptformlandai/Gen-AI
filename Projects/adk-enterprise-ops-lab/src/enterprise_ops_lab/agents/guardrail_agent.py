from __future__ import annotations

from enterprise_ops_lab.tools.guardrail_tools import input_check, output_check, tool_call_check


def check_input(query: str) -> dict:
    return input_check(query)


def check_output(text: str, confidence: float) -> dict:
    return output_check(text, confidence)


def check_tool(tool_name: str, approved: bool = False) -> dict:
    return tool_call_check(tool_name, approved=approved)

