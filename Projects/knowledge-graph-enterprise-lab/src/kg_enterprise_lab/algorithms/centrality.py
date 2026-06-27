"""Centrality metrics for critical service detection."""

from __future__ import annotations

from collections import defaultdict

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository


def degree_centrality(graph: InMemoryGraphRepository, label: str | None = None) -> dict[str, float]:
    candidates = graph.find_nodes(label=label) if label else list(graph.nodes.values())
    max_possible = max(len(graph.nodes) - 1, 1)
    return {
        node.id: round(len(graph.relationships_for_node(node.id, "both")) / max_possible, 4)
        for node in candidates
    }


def betweenness_centrality(graph: InMemoryGraphRepository, label: str | None = "Service") -> dict[str, float]:
    scores: dict[str, float] = defaultdict(float)
    services = graph.find_nodes(label=label) if label else list(graph.nodes.values())
    for source in services:
        for target in services:
            if source.id == target.id:
                continue
            path, _ = graph.shortest_path(source.id, target.id, max_depth=6)
            for middle in path[1:-1]:
                scores[middle] += 1.0
    normalizer = max(len(services) * max(len(services) - 1, 1), 1)
    return {node_id: round(score / normalizer, 4) for node_id, score in scores.items()}


def highest_dependency_centrality(graph: InMemoryGraphRepository) -> tuple[str, float] | None:
    scores = degree_centrality(graph, "Service")
    if not scores:
        return None
    return max(scores.items(), key=lambda item: item[1])
