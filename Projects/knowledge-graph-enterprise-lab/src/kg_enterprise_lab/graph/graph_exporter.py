"""Graph export helpers for JSON artifacts."""

from __future__ import annotations

import json
from pathlib import Path

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository


def export_json(graph: InMemoryGraphRepository, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(graph.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    return path
