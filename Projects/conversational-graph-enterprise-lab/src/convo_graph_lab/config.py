"""Runtime settings for conversational graph execution."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    data_dir: Path = PROJECT_ROOT / "data"
    export_dir: Path = PROJECT_ROOT / "data" / "exports"
    max_steps: int = 40
    max_node_retries: int = 2
    node_timeout_ms: int = 2500
    context_window_turns: int = 8


def get_settings() -> Settings:
    return Settings(
        data_dir=Path(os.getenv("CONV_GRAPH_DATA_DIR", PROJECT_ROOT / "data")),
        export_dir=Path(os.getenv("CONV_GRAPH_EXPORT_DIR", PROJECT_ROOT / "data" / "exports")),
        max_steps=int(os.getenv("CONV_GRAPH_MAX_STEPS", "40")),
        max_node_retries=int(os.getenv("CONV_GRAPH_MAX_NODE_RETRIES", "2")),
        node_timeout_ms=int(os.getenv("CONV_GRAPH_NODE_TIMEOUT_MS", "2500")),
        context_window_turns=int(os.getenv("CONV_GRAPH_CONTEXT_WINDOW_TURNS", "8")),
    )
