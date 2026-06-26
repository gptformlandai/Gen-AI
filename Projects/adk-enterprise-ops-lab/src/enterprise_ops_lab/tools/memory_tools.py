from __future__ import annotations

from pathlib import Path

from enterprise_ops_lab.memory.memory_service import InMemoryMemoryService


def add_resolution_note(text: str, service: str = "", memory_dir: str | Path = ".memory", tags: list[str] | None = None) -> dict:
    root = Path(__file__).resolve().parents[3]
    directory = Path(memory_dir)
    if not directory.is_absolute():
        directory = root / directory
    record = InMemoryMemoryService(directory).add(text, service=service, tags=tags or [])
    return record.model_dump(mode="json")


def search_resolution_notes(query: str, service: str = "", memory_dir: str | Path = ".memory") -> list[dict]:
    root = Path(__file__).resolve().parents[3]
    directory = Path(memory_dir)
    if not directory.is_absolute():
        directory = root / directory
    return [record.model_dump(mode="json") for record in InMemoryMemoryService(directory).search(query, service=service)]

