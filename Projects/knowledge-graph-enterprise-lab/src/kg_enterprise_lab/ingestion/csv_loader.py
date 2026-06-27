"""CSV loader for ownership and spreadsheet-style metadata."""

from __future__ import annotations

import csv
from pathlib import Path


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))
