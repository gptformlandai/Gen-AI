from __future__ import annotations

from dataclasses import dataclass, field

from enterprise_ops_lab.rag.document_loader import Document


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    source: str
    title: str
    text: str
    metadata: dict[str, str] = field(default_factory=dict)


def chunk_documents(documents: list[Document], max_words: int = 90, overlap: int = 15) -> list[Chunk]:
    chunks: list[Chunk] = []
    for doc in documents:
        words = doc.text.split()
        start = 0
        index = 1
        while start < len(words):
            end = min(start + max_words, len(words))
            text = " ".join(words[start:end])
            chunks.append(
                Chunk(
                    chunk_id=f"{doc.source}#{index:03d}",
                    source=doc.source,
                    title=doc.title,
                    text=text,
                    metadata=doc.metadata,
                )
            )
            if end == len(words):
                break
            start = max(0, end - overlap)
            index += 1
    return chunks

