"""Markdown source loader used by extraction and GraphRAG."""

from __future__ import annotations

from pathlib import Path

from kg_enterprise_lab.schemas.extraction import SourceDocument


def load_markdown(path: Path) -> SourceDocument:
    return SourceDocument(id=path.stem, source_type="markdown", text=path.read_text(encoding="utf-8"), metadata={"path": str(path)})
