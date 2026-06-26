from __future__ import annotations

import re

from baseline_rag_assistant.schemas import Chunk, Document


TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9_]+")


def tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text.lower())


def chunk_document(
    document: Document,
    max_words: int = 110,
    overlap_words: int = 20,
) -> list[Chunk]:
    """Create overlapping chunks while preserving readable original text."""

    words = document.text.split()
    if not words:
        return []
    if max_words <= overlap_words:
        raise ValueError("max_words must be greater than overlap_words.")

    chunks: list[Chunk] = []
    start = 0
    chunk_index = 0
    while start < len(words):
        end = min(start + max_words, len(words))
        chunks.append(
            Chunk(
                id=f"{document.id}::chunk-{chunk_index:03d}",
                document_id=document.id,
                title=document.title,
                text=" ".join(words[start:end]),
                chunk_index=chunk_index,
                metadata=document.metadata.copy(),
            )
        )
        if end == len(words):
            break
        start = end - overlap_words
        chunk_index += 1
    return chunks


def chunk_documents(documents: list[Document]) -> list[Chunk]:
    chunks: list[Chunk] = []
    for document in documents:
        chunks.extend(chunk_document(document))
    return chunks


def split_sentences(text: str) -> list[str]:
    """Small sentence splitter for extractive answer synthesis."""

    candidates = re.split(r"(?<=[.!?])\s+", text.strip())
    return [candidate.strip() for candidate in candidates if len(candidate.strip()) > 10]
