"""Entity resolver with aliases, fuzzy matching, and review queue output."""

from __future__ import annotations

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository
from kg_enterprise_lab.resolution.alias_manager import AliasManager
from kg_enterprise_lab.resolution.duplicate_detector import detect_duplicates
from kg_enterprise_lab.resolution.human_review_queue import HumanReviewItem, HumanReviewQueue
from kg_enterprise_lab.schemas.extraction import ExtractedEntity


class EntityResolver:
    def __init__(self, graph: InMemoryGraphRepository, review_threshold: float = 0.9) -> None:
        self.graph = graph
        self.review_threshold = review_threshold
        self.aliases = AliasManager()
        for node in graph.nodes.values():
            self.aliases.add_alias(node.name, node.id)
            self.aliases.add_alias(node.id, node.id)
            for alias in node.aliases:
                self.aliases.add_alias(alias, node.id)

    def resolve_name(self, name: str) -> str | None:
        direct = self.aliases.resolve(name)
        if direct:
            return direct
        lowered = name.lower()
        if len(lowered) < 4:
            return None
        for node in self.graph.nodes.values():
            names = {node.name.lower(), node.id.lower(), *(alias.lower() for alias in node.aliases)}
            if lowered in names:
                return node.id
        return None

    def resolve_entities(self, entities: list[ExtractedEntity]) -> tuple[dict[str, str], HumanReviewQueue]:
        mapping: dict[str, str] = {}
        review = HumanReviewQueue()
        for entity in entities:
            resolved = self.resolve_name(entity.name) or self.resolve_name(entity.canonical_id)
            if resolved:
                mapping[entity.canonical_id] = resolved
            if entity.confidence < self.review_threshold:
                review.add(HumanReviewItem(id=entity.canonical_id, reason="low_confidence_entity", candidates=[resolved or entity.name], confidence=entity.confidence))
        for left_id, right_id, score in detect_duplicates(self.graph):
            if score < 0.97:
                review.add(HumanReviewItem(id=f"{left_id}:{right_id}", reason="possible_duplicate", candidates=[left_id, right_id], confidence=score))
        return mapping, review
