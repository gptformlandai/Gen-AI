"""Cycle detection for directed service dependencies."""

from __future__ import annotations

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository


def detect_cycles(graph: InMemoryGraphRepository, relationship_types: set[str] | None = None) -> list[list[str]]:
    relationship_types = relationship_types or {"DEPENDS_ON", "CALLS"}
    cycles: list[list[str]] = []
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node_id: str, path: list[str]) -> None:
        if node_id in visiting:
            if node_id in path:
                cycles.append(path[path.index(node_id) :] + [node_id])
            return
        if node_id in visited:
            return
        visiting.add(node_id)
        for rel in graph.relationships_for_node(node_id, "out", relationship_types):
            visit(rel.target_id, path + [rel.target_id])
        visiting.remove(node_id)
        visited.add(node_id)

    for node in graph.find_nodes(label="Service"):
        visit(node.id, [node.id])
    return cycles
