"""Connected component detection."""

from __future__ import annotations

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository


def connected_components(graph: InMemoryGraphRepository) -> list[set[str]]:
    remaining = set(graph.nodes)
    components: list[set[str]] = []
    while remaining:
        start = remaining.pop()
        nodes, _ = graph.traverse(start, direction="both", max_depth=len(graph.nodes))
        components.append(nodes)
        remaining -= nodes
    return components
