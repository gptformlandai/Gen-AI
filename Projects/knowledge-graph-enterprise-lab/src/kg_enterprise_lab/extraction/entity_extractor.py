"""Entity extraction over architecture notes and runbooks."""

from __future__ import annotations

import re

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository
from kg_enterprise_lab.schemas.extraction import ExtractedEntity, SourceDocument


class EntityExtractor:
    def __init__(self, graph: InMemoryGraphRepository) -> None:
        self.graph = graph

    def extract(self, document: SourceDocument) -> list[ExtractedEntity]:
        text = document.text.lower()
        results: dict[str, ExtractedEntity] = {}
        for node in self.graph.nodes.values():
            candidates = [node.name, node.id, *node.aliases]
            if any(candidate and candidate.lower() in text for candidate in candidates):
                results[node.id] = ExtractedEntity(
                    canonical_id=node.id,
                    label=node.label,
                    name=node.name,
                    aliases=node.aliases,
                    confidence=0.92,
                    source_ref=document.id,
                    properties={"matched_by": "catalog_string"},
                )
        for incident_id in sorted(set(re.findall(r"\bINC-\d+\b", document.text))):
            node = self.graph.get_node(incident_id)
            results[incident_id] = ExtractedEntity(
                canonical_id=incident_id,
                label=node.label if node else "Incident",
                name=node.name if node else incident_id,
                confidence=0.98,
                source_ref=document.id,
                properties={"matched_by": "incident_regex"},
            )
        return sorted(results.values(), key=lambda item: (item.label, item.name))
