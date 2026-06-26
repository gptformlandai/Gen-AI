from __future__ import annotations

from pathlib import Path

from enterprise_ops_lab.rag.chunker import chunk_documents
from enterprise_ops_lab.rag.document_loader import load_markdown_documents
from enterprise_ops_lab.rag.vector_store import LocalVectorStore
from enterprise_ops_lab.schemas.incident import EvidenceItem


class RunbookRetriever:
    """RAG retriever over local runbooks with a Vertex RAG extension seam."""

    def __init__(self, runbook_dir: Path) -> None:
        documents = load_markdown_documents(runbook_dir)
        self.store = LocalVectorStore(chunk_documents(documents))

    def search(self, query: str, service: str = "", k: int = 4) -> list[EvidenceItem]:
        expanded = f"{query} {service}".strip()
        return self.store.search(expanded, k=k)

