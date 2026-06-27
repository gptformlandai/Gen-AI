"""Merge strategy for duplicate graph nodes."""

from __future__ import annotations

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository
from kg_enterprise_lab.schemas.relationship import GraphRelationship


def merge_duplicate_node(graph: InMemoryGraphRepository, canonical_id: str, duplicate_id: str) -> bool:
    canonical = graph.get_node(canonical_id)
    duplicate = graph.get_node(duplicate_id)
    if not canonical or not duplicate:
        return False
    canonical.aliases.extend(alias for alias in [duplicate.name, *duplicate.aliases] if alias not in canonical.aliases)
    canonical.properties.update({f"merged_{key}": value for key, value in duplicate.properties.items() if key not in canonical.properties})
    canonical.properties.setdefault("merged_duplicate_ids", [])
    if duplicate_id not in canonical.properties["merged_duplicate_ids"]:
        canonical.properties["merged_duplicate_ids"].append(duplicate_id)
    canonical.source_refs = sorted(set(canonical.source_refs + duplicate.source_refs))

    rewritten: list[GraphRelationship] = []
    seen_keys: set[tuple[str, str, str]] = set()
    for rel in list(graph.relationships.values()):
        source_id = canonical_id if rel.source_id == duplicate_id else rel.source_id
        target_id = canonical_id if rel.target_id == duplicate_id else rel.target_id
        if source_id == target_id:
            continue
        key = (source_id, rel.type, target_id)
        if key in seen_keys:
            continue
        seen_keys.add(key)
        rewritten.append(
            GraphRelationship(
                source_id=source_id,
                type=rel.type,
                target_id=target_id,
                properties=rel.properties,
                directed=rel.directed,
                source_refs=rel.source_refs,
                confidence=rel.confidence,
            )
        )
    graph.nodes.pop(duplicate_id, None)
    graph.replace_relationships(rewritten)
    return True
