from __future__ import annotations

from semantic_search_lab.embeddings import HashingTfidfEmbeddingModel, cosine_similarity
from semantic_search_lab.schemas import Chunk, SearchHit


def metadata_matches(metadata: dict[str, str], filters: dict[str, str] | None) -> bool:
    if not filters:
        return True
    return all(metadata.get(key) == value for key, value in filters.items())


class InMemoryVectorStore:
    """Exact vector-search baseline.

    Exact search scores every filtered chunk. It is the baseline we compare ANN
    against because it is simple, deterministic, and has no indexing shortcuts.
    """

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
    def from_chunks(
        cls,
        chunks: list[Chunk],
        embedding_model: HashingTfidfEmbeddingModel | None = None,
    ) -> "InMemoryVectorStore":
        model = embedding_model or HashingTfidfEmbeddingModel()
        model.fit([chunk.text for chunk in chunks])
        vectors = model.embed_many([chunk.text for chunk in chunks])
        return cls(chunks=chunks, vectors=vectors, embedding_model=model)

    def search(
        self,
        query: str,
        k: int = 5,
        filters: dict[str, str] | None = None,
        candidate_indices: list[int] | None = None,
    ) -> list[SearchHit]:
        query_vector = self.embedding_model.embed(query)
        indices = candidate_indices if candidate_indices is not None else list(range(len(self.chunks)))
        scored: list[tuple[float, Chunk]] = []

        for index in indices:
            chunk = self.chunks[index]
            if not metadata_matches(chunk.metadata, filters):
                continue
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
