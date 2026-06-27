"""API metadata loader."""

from __future__ import annotations

from pathlib import Path

from kg_enterprise_lab.ingestion.json_loader import load_json


def load_api_specs(path: Path) -> list[dict[str, object]]:
    return list(load_json(path))
