"""Entity linking for GraphRAG retrieval."""

from __future__ import annotations

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository
from kg_enterprise_lab.resolution.entity_resolver import EntityResolver


class EntityLinker:
    def __init__(self, graph: InMemoryGraphRepository) -> None:
        self.resolver = EntityResolver(graph)

    def link(self, question: str) -> list[str]:
        linked: list[str] = []
        lowered = question.lower()
        for token in question.replace("?", " ").replace(".", " ").split():
            if len(token) < 4 or token.lower() in {"with", "from", "that", "this", "slow", "why", "explain", "graphrag"}:
                continue
            resolved = self.resolver.resolve_name(token)
            if resolved and resolved not in linked:
                linked.append(resolved)
        for phrase in sorted(self.resolver.graph.nodes.values(), key=lambda node: len(node.name), reverse=True):
            if phrase.label in {"Schema", "DataEntity", "Endpoint", "ErrorCode"} and phrase.id.lower() not in lowered:
                continue
            if phrase.name.lower() in lowered and phrase.id not in linked:
                linked.append(phrase.id)
        return linked
