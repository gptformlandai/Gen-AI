"""Small PageRank-style algorithm for ranking critical graph nodes."""

from __future__ import annotations

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository


def pagerank(
    graph: InMemoryGraphRepository,
    relationship_types: set[str] | None = None,
    damping: float = 0.85,
    iterations: int = 25,
) -> dict[str, float]:
    if not graph.nodes:
        return {}
    node_ids = sorted(graph.nodes)
    score = {node_id: 1.0 / len(node_ids) for node_id in node_ids}
    for _ in range(iterations):
        next_score = {node_id: (1.0 - damping) / len(node_ids) for node_id in node_ids}
        for node_id in node_ids:
            outgoing = graph.relationships_for_node(node_id, "out", relationship_types)
            if not outgoing:
                share = damping * score[node_id] / len(node_ids)
                for target_id in node_ids:
                    next_score[target_id] += share
                continue
            share = damping * score[node_id] / len(outgoing)
            for rel in outgoing:
                if rel.target_id in next_score:
                    next_score[rel.target_id] += share
        score = next_score
    return {node_id: round(value, 6) for node_id, value in sorted(score.items(), key=lambda item: item[1], reverse=True)}
