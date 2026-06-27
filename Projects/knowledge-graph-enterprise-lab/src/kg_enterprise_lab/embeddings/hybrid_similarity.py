"""Hybrid graph plus vector similarity."""

from __future__ import annotations

from kg_enterprise_lab.algorithms.similarity import jaccard_similarity
from kg_enterprise_lab.embeddings.vector_index import LocalVectorIndex
from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository


def hybrid_node_search(graph: InMemoryGraphRepository, vector_index: LocalVectorIndex, query: str, anchor_id: str | None = None, top_k: int = 5) -> list[tuple[str, float]]:
    vector_hits = vector_index.search(query, top_k=top_k * 2)
    anchor_neighbors = {node.id for node in graph.neighbors(anchor_id)} if anchor_id else set()
    scored: list[tuple[str, float]] = []
    for hit in vector_hits:
        graph_score = 0.0
        if anchor_neighbors:
            graph_score = jaccard_similarity(anchor_neighbors, {node.id for node in graph.neighbors(hit.node_id)})
        scored.append((hit.node_id, round((0.75 * hit.score) + (0.25 * graph_score), 4)))
    return sorted(scored, key=lambda item: item[1], reverse=True)[:top_k]
