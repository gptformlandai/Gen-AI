"""Graphviz DOT exporter."""

from __future__ import annotations

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository


def export_dot(graph: InMemoryGraphRepository) -> str:
    lines = ["digraph enterprise_kg {"]
    for node in graph.nodes.values():
        label = f"{node.label}: {node.name}".replace('"', "'")
        lines.append(f'  "{node.id}" [label="{label}"];')
    for rel in graph.relationships.values():
        lines.append(f'  "{rel.source_id}" -> "{rel.target_id}" [label="{rel.type}"];')
    lines.append("}")
    return "\n".join(lines)
