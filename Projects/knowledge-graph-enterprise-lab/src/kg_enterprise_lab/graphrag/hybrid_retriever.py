"""Hybrid graph plus vector retrieval for GraphRAG."""

from __future__ import annotations

from kg_enterprise_lab.embeddings.hybrid_similarity import hybrid_node_search
from kg_enterprise_lab.embeddings.vector_index import LocalVectorIndex
from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository
from kg_enterprise_lab.schemas.graphrag import EvidenceChunk


class HybridRetriever:
    def __init__(self, graph: InMemoryGraphRepository, vector_index: LocalVectorIndex) -> None:
        self.graph = graph
        self.vector_index = vector_index

    def retrieve(self, question: str, anchor_ids: list[str], top_k: int = 5) -> list[EvidenceChunk]:
        anchor_id = anchor_ids[0] if anchor_ids else None
        hits = hybrid_node_search(self.graph, self.vector_index, question, anchor_id=anchor_id, top_k=top_k)
        evidence: list[EvidenceChunk] = []
        for node_id, score in hits:
            node = self.graph.get_node(node_id)
            if not node:
                continue
            evidence.append(
                EvidenceChunk(
                    id=f"hybrid-{node_id}",
                    source="hybrid",
                    text=f"{node.label} {node.name}: {node.properties}",
                    score=score,
                    node_ids=[node_id],
                )
            )
        return evidence
