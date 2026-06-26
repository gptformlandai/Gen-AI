from __future__ import annotations

from pathlib import Path


def list_trace_events(request_id: str, trace_dir: str | Path = ".traces") -> list[str]:
    root = Path(__file__).resolve().parents[3]
    directory = Path(trace_dir)
    if not directory.is_absolute():
        directory = root / directory
    path = directory / f"{request_id}.jsonl"
    if not path.exists():
        return []
    return path.read_text(encoding="utf-8").splitlines()

