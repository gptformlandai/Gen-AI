"""In-memory vector index for graph node retrieval."""

from __future__ import annotations

from dataclasses import dataclass, field

from kg_enterprise_lab.embeddings.embedding_service import HashingEmbeddingService, cosine_similarity
from kg_enterprise_lab.embeddings.node_embedding import node_to_text
from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository


@dataclass
class VectorHit:
    node_id: str
    score: float
    text: str


@dataclass
class LocalVectorIndex:
    embedding_service: HashingEmbeddingService = field(default_factory=HashingEmbeddingService)
    vectors: dict[str, list[float]] = field(default_factory=dict)
    texts: dict[str, str] = field(default_factory=dict)

    def index_graph(self, graph: InMemoryGraphRepository) -> None:
        for node in graph.nodes.values():
            text = node_to_text(node)
            self.texts[node.id] = text
            self.vectors[node.id] = self.embedding_service.embed(text)

    def search(self, query: str, top_k: int = 5) -> list[VectorHit]:
        query_vector = self.embedding_service.embed(query)
        hits = [
            VectorHit(node_id=node_id, score=round(cosine_similarity(query_vector, vector), 4), text=self.texts[node_id])
            for node_id, vector in self.vectors.items()
        ]
        return [hit for hit in sorted(hits, key=lambda item: item.score, reverse=True) if hit.score > 0][:top_k]
