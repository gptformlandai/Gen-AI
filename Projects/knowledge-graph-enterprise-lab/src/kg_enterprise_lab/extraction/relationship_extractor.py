"""Rule-based relationship extraction from architecture text."""

from __future__ import annotations

import re

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository
from kg_enterprise_lab.schemas.extraction import ExtractedRelationship, SourceDocument


class RelationshipExtractor:
    def __init__(self, graph: InMemoryGraphRepository) -> None:
        self.graph = graph

    def extract(self, document: SourceDocument) -> list[ExtractedRelationship]:
        text = " ".join(document.text.replace("\n", " ").split())
        names = sorted({node.name for node in self.graph.nodes.values()} | {node.id for node in self.graph.nodes.values()}, key=len, reverse=True)
        results: list[ExtractedRelationship] = []
        for source_name in names:
            escaped_source = re.escape(source_name)
            for verb, rel_type in [
                ("calls", "CALLS"),
                ("depends on", "DEPENDS_ON"),
                ("reads", "READS_FROM"),
                ("writes", "WRITES_TO"),
                ("publishes", "PUBLISHES_TO"),
                ("consumes", "CONSUMES_FROM"),
            ]:
                pattern = re.compile(rf"\b{escaped_source}\b[^.]*?\b{verb}\b[^.]*?\b([^.,;]+)", re.IGNORECASE)
                for match in pattern.finditer(text):
                    target_phrase = match.group(1).strip()
                    target = self._find_target(target_phrase, names)
                    if target:
                        results.append(
                            ExtractedRelationship(
                                source_name=source_name,
                                relationship_type=rel_type,
                                target_name=target,
                                confidence=0.78,
                                source_ref=document.id,
                                evidence=match.group(0)[:240],
                            )
                        )
        return _dedupe(results)

    def _find_target(self, phrase: str, names: list[str]) -> str | None:
        lowered = phrase.lower()
        for name in names:
            if name.lower() in lowered:
                return name
        return None


def _dedupe(items: list[ExtractedRelationship]) -> list[ExtractedRelationship]:
    seen: set[tuple[str, str, str]] = set()
    deduped: list[ExtractedRelationship] = []
    for item in items:
        key = (item.source_name.lower(), item.relationship_type, item.target_name.lower())
        if key not in seen:
            seen.add(key)
            deduped.append(item)
    return deduped
