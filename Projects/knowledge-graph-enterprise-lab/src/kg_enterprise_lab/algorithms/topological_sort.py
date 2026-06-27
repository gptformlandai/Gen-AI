"""Topological sort over dependency-like relationships."""

from __future__ import annotations

from collections import defaultdict, deque

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository


def topological_sort(graph: InMemoryGraphRepository, relationship_types: set[str] | None = None) -> list[str]:
    relationship_types = relationship_types or {"DEPENDS_ON"}
    nodes = [node.id for node in graph.find_nodes(label="Service")]
    indegree = {node_id: 0 for node_id in nodes}
    outgoing: dict[str, list[str]] = defaultdict(list)
    for rel in graph.relationships.values():
        if rel.type in relationship_types and rel.source_id in indegree and rel.target_id in indegree:
            outgoing[rel.source_id].append(rel.target_id)
            indegree[rel.target_id] += 1
    queue: deque[str] = deque(sorted(node_id for node_id, count in indegree.items() if count == 0))
    order: list[str] = []
    while queue:
        node_id = queue.popleft()
        order.append(node_id)
        for target_id in outgoing[node_id]:
            indegree[target_id] -= 1
            if indegree[target_id] == 0:
                queue.append(target_id)
    return order
