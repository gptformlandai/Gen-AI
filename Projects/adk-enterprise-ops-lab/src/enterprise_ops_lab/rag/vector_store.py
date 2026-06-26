from __future__ import annotations

from dataclasses import dataclass

from enterprise_ops_lab.rag.chunker import Chunk
from enterprise_ops_lab.rag.embeddings import cosine, embed_text, tokenize
from enterprise_ops_lab.schemas.incident import EvidenceItem


@dataclass
class IndexedChunk:
    chunk: Chunk
    vector: dict[str, float]


class LocalVectorStore:
    """Small vector-store simulation for local RAG demos and tests."""

    def __init__(self, chunks: list[Chunk]) -> None:
        self.index = [IndexedChunk(chunk=chunk, vector=embed_text(f"{chunk.title} {chunk.text} {' '.join(chunk.metadata.values())}")) for chunk in chunks]

    def search(self, query: str, k: int = 4, threshold: float = 0.04) -> list[EvidenceItem]:
        query_vector = embed_text(query)
        query_tokens = set(tokenize(query))
        scored: list[EvidenceItem] = []
        for indexed in self.index:
            lexical_overlap = len(query_tokens & set(tokenize(indexed.chunk.text + " " + indexed.chunk.title)))
            metadata_boost = 0.05 if any(token in " ".join(indexed.chunk.metadata.values()).lower() for token in query_tokens) else 0.0
            score = cosine(query_vector, indexed.vector) + (0.03 * lexical_overlap) + metadata_boost
            if score >= threshold:
                scored.append(
                    EvidenceItem(
                        source=indexed.chunk.source,
                        title=indexed.chunk.title,
                        quote=indexed.chunk.text,
                        score=round(score, 4),
                        metadata={**indexed.chunk.metadata, "chunk_id": indexed.chunk.chunk_id},
                    )
                )
        return sorted(scored, key=lambda item: item.score, reverse=True)[:k]

