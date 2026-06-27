"""Combined rule-based extractor for local, deterministic execution."""

from __future__ import annotations

from kg_enterprise_lab.extraction.entity_extractor import EntityExtractor
from kg_enterprise_lab.extraction.relationship_extractor import RelationshipExtractor
from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository
from kg_enterprise_lab.schemas.extraction import ExtractionBatch, SourceDocument


class RuleBasedExtractor:
    def __init__(self, graph: InMemoryGraphRepository) -> None:
        self.entity_extractor = EntityExtractor(graph)
        self.relationship_extractor = RelationshipExtractor(graph)

    def extract(self, document: SourceDocument) -> ExtractionBatch:
        return ExtractionBatch(
            entities=self.entity_extractor.extract(document),
            relationships=self.relationship_extractor.extract(document),
        )
