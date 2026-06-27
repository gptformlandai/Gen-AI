"""Vector retrieval for hybrid RAG."""

from __future__ import annotations

from kg_enterprise_lab.embeddings.vector_index import LocalVectorIndex
from kg_enterprise_lab.schemas.graphrag import EvidenceChunk


class VectorRetriever:
    def __init__(self, index: LocalVectorIndex) -> None:
        self.index = index

    def retrieve(self, question: str, top_k: int = 5) -> list[EvidenceChunk]:
        return [
            EvidenceChunk(id=f"vector-{hit.node_id}", source="vector", text=hit.text, score=hit.score, node_ids=[hit.node_id])
            for hit in self.index.search(question, top_k=top_k)
        ]
