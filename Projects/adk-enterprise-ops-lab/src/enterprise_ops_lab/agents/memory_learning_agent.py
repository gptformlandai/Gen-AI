from __future__ import annotations

from enterprise_ops_lab.tools.memory_tools import add_resolution_note, search_resolution_notes


def remember(text: str, service: str = "", memory_dir: str = ".memory") -> dict:
    return add_resolution_note(text, service=service, memory_dir=memory_dir, tags=["resolution"])


def recall(query: str, service: str = "", memory_dir: str = ".memory") -> list[dict]:
    return search_resolution_notes(query, service=service, memory_dir=memory_dir)

