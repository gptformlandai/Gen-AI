"""Shortest-path helper."""

from __future__ import annotations

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository


def find_shortest_path(graph: InMemoryGraphRepository, source_id: str, target_id: str, max_depth: int = 6) -> list[str]:
    path, _ = graph.shortest_path(source_id, target_id, max_depth=max_depth)
    return path
