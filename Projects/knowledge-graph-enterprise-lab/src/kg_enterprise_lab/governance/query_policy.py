"""Query policy allowlist and traversal limits."""

from __future__ import annotations

ALLOWED_INTENTS = {
    "dependents",
    "blast_radius",
    "shortest_path",
    "ownership",
    "similar_incidents",
    "runbook_search",
    "lineage",
    "centrality",
    "validate",
    "duplicates",
    "rdf_compare",
    "generic",
}


def is_allowed_intent(intent: str) -> bool:
    return intent in ALLOWED_INTENTS
