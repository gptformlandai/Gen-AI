"""API dependency providers."""

from __future__ import annotations

from functools import lru_cache

from kg_enterprise_lab.ingestion.ingestion_pipeline import build_sample_graph


@lru_cache(maxsize=1)
def get_graph():
    return build_sample_graph()
