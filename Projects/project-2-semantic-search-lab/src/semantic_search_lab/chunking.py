from __future__ import annotations

import re

from semantic_search_lab.schemas import Chunk, Document


TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9_]+")


def tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text.lower())


def chunk_document(
    document: Document,
    max_tokens: int = 120,
    overlap_tokens: int = 20,
) -> list[Chunk]:
    """Split one document into overlapping chunks.

    Overlap preserves local context across chunk boundaries. Too much overlap
    increases storage and duplicate retrieval; too little can split facts apart.
    """

    tokens = tokenize(document.text)
    if not tokens:
        return []

    if max_tokens <= overlap_tokens:
        raise ValueError("max_tokens must be greater than overlap_tokens.")

    chunks: list[Chunk] = []
    start = 0
    chunk_index = 0
    while start < len(tokens):
        end = min(start + max_tokens, len(tokens))
        chunk_tokens = tokens[start:end]
        chunks.append(
            Chunk(
                id=f"{document.id}::chunk-{chunk_index:03d}",
                document_id=document.id,
                title=document.title,
                text=" ".join(chunk_tokens),
                chunk_index=chunk_index,
                metadata=document.metadata.copy(),
            )
        )
        if end == len(tokens):
            break
        start = end - overlap_tokens
        chunk_index += 1
    return chunks


def chunk_documents(
    documents: list[Document],
    max_tokens: int = 120,
    overlap_tokens: int = 20,
) -> list[Chunk]:
    chunks: list[Chunk] = []
    for document in documents:
        chunks.extend(chunk_document(document, max_tokens=max_tokens, overlap_tokens=overlap_tokens))
    return chunks
