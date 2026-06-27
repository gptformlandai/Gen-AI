"""Node text construction for embedding."""

from __future__ import annotations

from kg_enterprise_lab.schemas.node import GraphNode


def node_to_text(node: GraphNode) -> str:
    property_text = " ".join(str(value) for value in node.properties.values())
    return f"{node.label} {node.name} {' '.join(node.aliases)} {property_text}"
