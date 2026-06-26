from __future__ import annotations


def route_intent(intent: str) -> str:
    routes = {
        "search_runbook": "rag_runbook_agent",
        "remember_resolution": "memory_learning_agent",
        "generate_report": "artifact_report_agent",
        "evaluate_trajectory": "evaluator_agent",
        "show_tool_trace": "root_incident_coordinator_agent",
        "demonstrate_state_memory": "memory_learning_agent",
    }
    return routes.get(intent, "investigation_workflow_agent")

