"""Local graph indexes for fast name and label lookups."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository


@dataclass
class GraphIndexes:
    by_label: dict[str, list[str]] = field(default_factory=lambda: defaultdict(list))
    by_name: dict[str, str] = field(default_factory=dict)
    aliases: dict[str, str] = field(default_factory=dict)


def build_indexes(graph: InMemoryGraphRepository) -> GraphIndexes:
    indexes = GraphIndexes()
    for node in graph.nodes.values():
        indexes.by_label[node.label].append(node.id)
        indexes.by_name[node.name.lower()] = node.id
        indexes.by_name[node.id.lower()] = node.id
        for alias in node.aliases:
            indexes.aliases[alias.lower()] = node.id
    return indexes
