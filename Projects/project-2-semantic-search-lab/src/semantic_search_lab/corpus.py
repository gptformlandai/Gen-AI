from __future__ import annotations

import json
from pathlib import Path

from semantic_search_lab.schemas import Document


def read_jsonl_documents(path: Path) -> list[Document]:
    """Load JSONL documents from disk."""

    documents: list[Document] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                documents.append(Document.model_validate_json(line))
            except Exception as error:
                raise ValueError(f"Invalid document at {path}:{line_number}: {error}") from error
    return documents


def write_jsonl_documents(path: Path, documents: list[Document]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for document in documents:
            handle.write(json.dumps(document.model_dump(mode="json"), sort_keys=True) + "\n")
