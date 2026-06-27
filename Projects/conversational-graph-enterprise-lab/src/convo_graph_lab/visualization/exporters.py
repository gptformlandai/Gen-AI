"""Mermaid, Graphviz, and JSON visualization exports."""

from __future__ import annotations

import re

from convo_graph_lab.schema.models import GraphDefinition, TraceEvent


def _safe_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", value)


def export_graph_mermaid(graph: GraphDefinition, trace: list[TraceEvent] | None = None) -> str:
    visited = {event.node_id for event in trace or []}
    lines = ["flowchart TD"]
    for node in graph.nodes:
        marker = " *" if node.id in visited else ""
        lines.append(f'  {_safe_id(node.id)}["{node.type}: {node.name}{marker}"]')
    for edge in graph.edges:
        lines.append(f"  {_safe_id(edge.source)} -->|{edge.condition}| {_safe_id(edge.target)}")
    return "\n".join(lines)


def export_graph_dot(graph: GraphDefinition, trace: list[TraceEvent] | None = None) -> str:
    visited = {event.node_id for event in trace or []}
    lines = ["digraph conversational_graph {"]
    for node in graph.nodes:
        color = "green" if node.id in visited else "black"
        lines.append(f'  "{node.id}" [label="{node.type}: {node.name}", color="{color}"];')
    for edge in graph.edges:
        lines.append(f'  "{edge.source}" -> "{edge.target}" [label="{edge.condition}"];')
    lines.append("}")
    return "\n".join(lines)


def export_graph_json(graph: GraphDefinition, trace: list[TraceEvent] | None = None) -> dict[str, object]:
    visited = [event.node_id for event in trace or []]
    return {
        "nodes": [node.model_dump() for node in graph.nodes],
        "edges": [edge.model_dump() for edge in graph.edges],
        "visited_node_ids": visited,
        "transition_history": [event.model_dump() for event in trace or []],
    }
