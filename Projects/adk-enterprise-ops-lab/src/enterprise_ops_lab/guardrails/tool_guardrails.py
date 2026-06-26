from __future__ import annotations


APPROVAL_REQUIRED = {"cancel_database_query", "rollback_deployment", "scale_production"}


def validate_tool_call(tool_name: str, approved: bool = False) -> tuple[bool, str]:
    if tool_name in APPROVAL_REQUIRED and not approved:
        return False, f"{tool_name} requires human approval"
    return True, "tool call accepted"

