from __future__ import annotations

from enterprise_ops_lab.callbacks.lifecycle_callbacks import CallbackManager


def record_safety_callback(callbacks: CallbackManager, request_id: str, session_id: str, agent_name: str, outcome: str, reason: str) -> None:
    callbacks.safety(request_id, session_id, agent_name, outcome, reason)

