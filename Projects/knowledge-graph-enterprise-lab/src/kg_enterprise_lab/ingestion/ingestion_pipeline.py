"""End-to-end ingestion pipeline for the enterprise sample graph."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from kg_enterprise_lab.config import Settings, get_settings
from kg_enterprise_lab.graph.graph_builder import build_graph_from_sources
from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository
from kg_enterprise_lab.ingestion.json_loader import load_json
from kg_enterprise_lab.ingestion.markdown_loader import load_markdown
from kg_enterprise_lab.schemas.extraction import SourceDocument
from kg_enterprise_lab.schemas.ingestion import IngestionReport, SourceIngestionStats


RAW_FILES = {
    "services": "services.json",
    "apis": "apis.json",
    "databases": "databases.json",
    "kafka_topics": "kafka_topics.json",
    "teams": "teams.json",
    "owners": "owners.json",
    "incidents": "incidents.json",
    "deployments": "deployments.json",
    "runbooks": "runbooks.json",
    "business_capabilities": "business_capabilities.json",
    "environments": "environments.json",
}


def load_enterprise_sources(settings: Settings | None = None) -> dict[str, Any]:
    settings = settings or get_settings()
    raw_dir = settings.data_dir / "raw"
    sources: dict[str, Any] = {}
    for key, filename in RAW_FILES.items():
        path = raw_dir / filename
        sources[key] = load_json(path) if path.exists() else []
    notes_path = raw_dir / "architecture_notes.md"
    sources["documents"] = [load_markdown(notes_path)] if notes_path.exists() else []
    return sources


def build_sample_graph(settings: Settings | None = None) -> InMemoryGraphRepository:
    sources = load_enterprise_sources(settings)
    return build_graph_from_sources(sources)


def build_ingestion_report(settings: Settings | None = None) -> IngestionReport:
    settings = settings or get_settings()
    sources = load_enterprise_sources(settings)
    graph = build_graph_from_sources(sources)
    stats: list[SourceIngestionStats] = []
    for source_name, records in sorted(sources.items()):
        if source_name == "documents":
            continue
        stats.append(
            SourceIngestionStats(
                source_name=source_name,
                record_count=len(records),
                checksum=_checksum(records),
            )
        )
    warnings = []
    if not sources.get("services"):
        warnings.append("No service records loaded.")
    if not sources.get("incidents"):
        warnings.append("No incident records loaded.")
    return IngestionReport(
        source_stats=stats,
        document_count=len(sources.get("documents", [])),
        node_count=len(graph.nodes),
        relationship_count=len(graph.relationships),
        warnings=warnings,
    )


def load_documents(settings: Settings | None = None) -> list[SourceDocument]:
    settings = settings or get_settings()
    raw_dir = Path(settings.data_dir) / "raw"
    return [load_markdown(path) for path in raw_dir.glob("*.md")]


def _checksum(records: Any) -> str:
    payload = json.dumps(records, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
