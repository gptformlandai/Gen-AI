"""Conversation execution debugger."""

from __future__ import annotations

from convo_graph_lab.schema.models import ConversationState, StateSnapshot, TraceEvent
from convo_graph_lab.workflows.pattern_detector import detect_patterns


def build_debug_report(state: ConversationState, trace: list[TraceEvent], snapshots: list[StateSnapshot]) -> dict[str, object]:
    failures = [event for event in trace if event.status == "failed" or event.error]
    slow_nodes = sorted(trace, key=lambda event: event.latency_ms, reverse=True)[:5]
    return {
        "session_id": state.session_id,
        "status": state.status,
        "current_node_id": state.current_node_id,
        "path": state.visited_node_ids,
        "detected_patterns": detect_patterns(state.visited_node_ids),
        "selected_transitions": [
            {"node_id": event.node_id, "edge_id": event.selected_edge_id, "next_node_id": event.next_node_id}
            for event in trace
            if event.selected_edge_id
        ],
        "failures": [event.model_dump() for event in failures],
        "slow_nodes": [
            {"node_id": event.node_id, "node_type": event.node_type, "latency_ms": event.latency_ms}
            for event in slow_nodes
        ],
        "snapshots": [snapshot.model_dump() for snapshot in snapshots],
        "errors": list(state.context.errors),
    }
