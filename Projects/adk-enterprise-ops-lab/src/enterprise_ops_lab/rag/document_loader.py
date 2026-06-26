from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Document:
    source: str
    title: str
    text: str
    metadata: dict[str, str] = field(default_factory=dict)


def load_markdown_documents(directory: Path) -> list[Document]:
    documents: list[Document] = []
    for path in sorted(directory.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        metadata, body = split_front_matter(raw)
        title = next((line.lstrip("# ").strip() for line in body.splitlines() if line.startswith("# ")), path.stem)
        documents.append(Document(source=path.name, title=title, text=body.strip(), metadata=metadata))
    return documents


def split_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    metadata = {}
    for line in parts[1].strip().splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()
    return metadata, parts[2]

