from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4
import json

from enterprise_ops_lab.schemas.memory import MemoryRecord


class InMemoryMemoryService:
    """Long-term resolution note store with a persistent-backend extension seam."""

    def __init__(self, memory_dir: Path | None = None) -> None:
        self.memory_dir = memory_dir
        self.records: list[MemoryRecord] = []
        if memory_dir:
            memory_dir.mkdir(parents=True, exist_ok=True)
            self._load()

    def add(self, text: str, service: str = "", tags: list[str] | None = None) -> MemoryRecord:
        record = MemoryRecord(
            memory_id=f"mem-{uuid4().hex[:8]}",
            text=text,
            tags=tags or [],
            service=service,
            created_at=datetime.now(UTC).replace(microsecond=0).isoformat(),
        )
        self.records.append(record)
        self._save()
        return record

    def search(self, query: str, service: str = "", k: int = 3) -> list[MemoryRecord]:
        q = set(query.lower().split())
        scored: list[MemoryRecord] = []
        for record in self.records:
            haystack = f"{record.text} {' '.join(record.tags)} {record.service}".lower()
            score = len(q & set(haystack.split()))
            if service and record.service == service:
                score += 2
            if score:
                scored.append(record.model_copy(update={"score": float(score)}))
        return sorted(scored, key=lambda item: item.score, reverse=True)[:k]

    def summarize(self, service: str = "") -> str:
        records = [record for record in self.records if not service or record.service == service]
        if not records:
            return "No durable resolution memories found."
        return "; ".join(record.text for record in records[-3:])

    def _load(self) -> None:
        path = self.memory_dir / "memory.json" if self.memory_dir else None
        if path and path.exists():
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.records = [MemoryRecord.model_validate(item) for item in payload]

    def _save(self) -> None:
        if not self.memory_dir:
            return
        path = self.memory_dir / "memory.json"
        path.write_text(json.dumps([record.model_dump() for record in self.records], indent=2), encoding="utf-8")

