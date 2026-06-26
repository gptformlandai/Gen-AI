from __future__ import annotations

from enterprise_ops_lab.tools.rag_tools import search_runbooks


def run(query: str, service: str = "") -> dict:
    """Specialist RAG agent behavior."""
    return search_runbooks(query, service=service)

