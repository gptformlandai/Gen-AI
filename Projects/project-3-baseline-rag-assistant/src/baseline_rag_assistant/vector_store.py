from __future__ import annotations

from baseline_rag_assistant.embeddings import HashingTfidfEmbeddingModel, cosine_similarity
from baseline_rag_assistant.schemas import Chunk, SearchHit


class InMemoryVectorStore:
    """Exact retrieval baseline for Project 3 RAG."""

    def __init__(
        self,
        chunks: list[Chunk],
        vectors: list[list[float]],
        embedding_model: HashingTfidfEmbeddingModel,
    ) -> None:
        if len(chunks) != len(vectors):
            raise ValueError("chunks and vectors must have the same length.")
        self.chunks = chunks
        self.vectors = vectors
        self.embedding_model = embedding_model

    @classmethod
    def from_chunks(cls, chunks: list[Chunk]) -> "InMemoryVectorStore":
        model = HashingTfidfEmbeddingModel()
        model.fit([chunk.text for chunk in chunks])
        return cls(chunks, model.embed_many([chunk.text for chunk in chunks]), model)

    def search(self, query: str, k: int = 5) -> list[SearchHit]:
        query_vector = self.embedding_model.embed(query)
        scored: list[tuple[float, Chunk]] = []
        for index, chunk in enumerate(self.chunks):
            score = cosine_similarity(query_vector, self.vectors[index])
            scored.append((score, chunk))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [
            SearchHit(
                chunk_id=chunk.id,
                document_id=chunk.document_id,
                title=chunk.title,
                score=round(score, 6),
                text=chunk.text,
                metadata=chunk.metadata,
            )
            for score, chunk in scored[:k]
        ]
