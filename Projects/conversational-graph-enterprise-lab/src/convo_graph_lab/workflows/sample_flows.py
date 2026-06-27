"""Named sample conversational patterns supported by the lab."""

from __future__ import annotations


CONVERSATIONAL_PATTERNS = {
    "greeting_flow": ["input", "intent_router"],
    "intent_detection_flow": ["input", "intent_router"],
    "clarification_loop": ["clarify", "collect_slot", "intent_router"],
    "disambiguation_loop": ["clarify", "collect_slot"],
    "multi_step_workflow": ["workflow_agent", "user_profile", "memory_write", "decision"],
    "error_recovery": ["search", "retry_tool", "fallback"],
    "human_handoff": ["decision", "human_approval"],
    "multi_agent_workflow": ["intent_router", "incident_agent", "developer_agent", "summary"],
    "interrupt_resume": ["human_approval", "end"],
}
