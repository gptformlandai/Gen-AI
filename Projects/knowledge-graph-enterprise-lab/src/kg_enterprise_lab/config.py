"""Runtime settings for local and production-style execution."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    data_dir: Path = PROJECT_ROOT / "data"
    export_dir: Path = PROJECT_ROOT / "data" / "exports"
    graph_state_path: Path = PROJECT_ROOT / "data" / "exports" / "graph_state.json"
    max_traversal_depth: int = 4
    min_confidence: float = 0.65
    redaction_enabled: bool = True
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "change-me"
    rdf_endpoint_url: str = "http://localhost:3030/enterprise"


def get_settings() -> Settings:
    return Settings(
        data_dir=Path(os.getenv("KG_LAB_DATA_DIR", PROJECT_ROOT / "data")),
        export_dir=Path(os.getenv("KG_LAB_EXPORT_DIR", PROJECT_ROOT / "data" / "exports")),
        graph_state_path=Path(os.getenv("KG_LAB_GRAPH_STATE", PROJECT_ROOT / "data" / "exports" / "graph_state.json")),
        max_traversal_depth=int(os.getenv("KG_LAB_MAX_TRAVERSAL_DEPTH", "4")),
        min_confidence=float(os.getenv("KG_LAB_MIN_CONFIDENCE", "0.65")),
        redaction_enabled=os.getenv("KG_LAB_REDACTION_ENABLED", "true").lower() == "true",
        neo4j_uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        neo4j_user=os.getenv("NEO4J_USER", "neo4j"),
        neo4j_password=os.getenv("NEO4J_PASSWORD", "change-me"),
        rdf_endpoint_url=os.getenv("RDF_ENDPOINT_URL", "http://localhost:3030/enterprise"),
    )
