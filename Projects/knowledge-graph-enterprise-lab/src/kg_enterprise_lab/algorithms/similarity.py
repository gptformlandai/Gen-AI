"""Graph-neighborhood similarity scoring."""

from __future__ import annotations

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository


def jaccard_similarity(left: set[str], right: set[str]) -> float:
    if not left and not right:
        return 1.0
    return len(left & right) / max(len(left | right), 1)


def similar_nodes(graph: InMemoryGraphRepository, node_id: str, label: str | None = None, top_k: int = 5) -> list[tuple[str, float]]:
    base_neighbors = {node.id for node in graph.neighbors(node_id)}
    scores: list[tuple[str, float]] = []
    for candidate in graph.find_nodes(label=label):
        if candidate.id == node_id:
            continue
        score = jaccard_similarity(base_neighbors, {node.id for node in graph.neighbors(candidate.id)})
        if score > 0:
            scores.append((candidate.id, round(score, 3)))
    return sorted(scores, key=lambda item: item[1], reverse=True)[:top_k]
