from __future__ import annotations

from pathlib import Path

from enterprise_ops_lab.rag.grounded_generator import generate_grounded_answer
from enterprise_ops_lab.rag.retriever import RunbookRetriever


def search_runbooks(query: str, service: str = "", runbook_dir: str | Path = "data/runbooks") -> dict:
    root = Path(__file__).resolve().parents[3]
    directory = Path(runbook_dir)
    if not directory.is_absolute():
        directory = root / directory
    retriever = RunbookRetriever(directory)
    evidence = retriever.search(query, service=service)
    return {
        "answer": generate_grounded_answer(query, evidence),
        "evidence": [item.model_dump(mode="json") for item in evidence],
        "sources": sorted({item.source for item in evidence}),
    }

