from __future__ import annotations

from enterprise_ops_lab.callbacks.lifecycle_callbacks import CallbackManager


def record_tool_callback(callbacks: CallbackManager, request_id: str, session_id: str, agent_name: str, tool_name: str) -> None:
    callbacks.before_tool(request_id, session_id, agent_name, tool_name)

