"""Lightweight natural-language intent classifier."""

from __future__ import annotations


def classify_intent(question: str) -> str:
    text = question.lower()
    if "blast radius" in text or "impacted" in text:
        return "blast_radius"
    if "shortest path" in text or "path between" in text:
        return "shortest_path"
    if "depend on" in text or "depends on" in text or "dependents" in text:
        return "dependents"
    if "team owns" in text or "owners" in text or "contacted" in text:
        return "ownership"
    if "similar" in text and "incident" in text:
        return "similar_incidents"
    if "runbooks" in text or "runbook" in text:
        return "runbook_search"
    if "lineage" in text:
        return "lineage"
    if "highest" in text and "centrality" in text:
        return "centrality"
    if "validate" in text:
        return "validate"
    if "duplicate" in text:
        return "duplicates"
    if "rdf" in text or "sparql" in text:
        return "rdf_compare"
    return "generic"
