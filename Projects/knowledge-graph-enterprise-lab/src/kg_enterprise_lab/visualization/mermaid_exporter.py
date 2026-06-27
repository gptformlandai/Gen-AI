"""Mermaid graph exporter."""

from __future__ import annotations

import re

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository


def mermaid_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", value)


def export_mermaid(graph: InMemoryGraphRepository, title: str = "Enterprise Knowledge Graph") -> str:
    lines = ["flowchart LR", f"  %% {title}"]
    for node in graph.nodes.values():
        label = f"{node.label}: {node.name}".replace('"', "'")
        lines.append(f'  {mermaid_id(node.id)}["{label}"]')
    for rel in graph.relationships.values():
        lines.append(f"  {mermaid_id(rel.source_id)} -->|{rel.type}| {mermaid_id(rel.target_id)}")
    return "\n".join(lines)
