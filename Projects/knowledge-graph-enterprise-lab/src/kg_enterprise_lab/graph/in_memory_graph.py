"""Production-shaped in-memory graph repository for local execution."""

from __future__ import annotations

import json
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

from kg_enterprise_lab.schemas.node import GraphNode
from kg_enterprise_lab.schemas.relationship import GraphRelationship


class InMemoryGraphRepository:
    def __init__(self) -> None:
        self.nodes: dict[str, GraphNode] = {}
        self.relationships: dict[str, GraphRelationship] = {}
        self.outbound: dict[str, set[str]] = defaultdict(set)
        self.inbound: dict[str, set[str]] = defaultdict(set)

    def upsert_node(self, node: GraphNode) -> GraphNode:
        existing = self.nodes.get(node.id)
        if existing:
            merged_properties = {**existing.properties, **node.properties}
            aliases = sorted(set(existing.aliases + node.aliases))
            source_refs = sorted(set(existing.source_refs + node.source_refs))
            node = existing.model_copy(update={"properties": merged_properties, "aliases": aliases, "source_refs": source_refs})
        self.nodes[node.id] = node
        return node

    def upsert_relationship(self, relationship: GraphRelationship) -> GraphRelationship:
        self.relationships[relationship.id] = relationship
        self.outbound[relationship.source_id].add(relationship.id)
        self.inbound[relationship.target_id].add(relationship.id)
        return relationship

    def replace_relationships(self, relationships: list[GraphRelationship]) -> None:
        self.relationships.clear()
        self.outbound.clear()
        self.inbound.clear()
        for relationship in relationships:
            self.upsert_relationship(relationship)

    def get_node(self, node_id: str) -> GraphNode | None:
        return self.nodes.get(node_id)

    def get_relationship(self, relationship_id: str) -> GraphRelationship | None:
        return self.relationships.get(relationship_id)

    def find_nodes(self, label: str | None = None, name: str | None = None) -> list[GraphNode]:
        normalized_name = name.lower().strip() if name else None
        results: list[GraphNode] = []
        for node in self.nodes.values():
            if label and node.label != label:
                continue
            if normalized_name:
                names = {node.name.lower(), node.id.lower(), *(alias.lower() for alias in node.aliases)}
                if normalized_name not in names and normalized_name not in node.searchable_text():
                    continue
            results.append(node)
        return sorted(results, key=lambda item: (item.label, item.name))

    def relationships_for_node(
        self,
        node_id: str,
        direction: str = "both",
        relationship_types: set[str] | None = None,
    ) -> list[GraphRelationship]:
        rel_ids: set[str] = set()
        if direction in {"out", "both"}:
            rel_ids.update(self.outbound.get(node_id, set()))
        if direction in {"in", "both"}:
            rel_ids.update(self.inbound.get(node_id, set()))
        rels = [self.relationships[rel_id] for rel_id in rel_ids]
        if relationship_types:
            rels = [rel for rel in rels if rel.type in relationship_types]
        return sorted(rels, key=lambda rel: (rel.type, rel.source_id, rel.target_id))

    def neighbors(
        self,
        node_id: str,
        direction: str = "both",
        relationship_types: set[str] | None = None,
    ) -> list[GraphNode]:
        nodes: list[GraphNode] = []
        for rel in self.relationships_for_node(node_id, direction, relationship_types):
            other_id = rel.target_id if rel.source_id == node_id else rel.source_id
            node = self.get_node(other_id)
            if node:
                nodes.append(node)
        return sorted({node.id: node for node in nodes}.values(), key=lambda node: node.name)

    def shortest_path(
        self,
        source_id: str,
        target_id: str,
        relationship_types: set[str] | None = None,
        max_depth: int = 6,
    ) -> tuple[list[str], list[str]]:
        queue: deque[tuple[str, list[str], list[str]]] = deque([(source_id, [source_id], [])])
        seen = {source_id}
        while queue:
            current, path, rel_path = queue.popleft()
            if current == target_id:
                return path, rel_path
            if len(path) > max_depth:
                continue
            for rel in self.relationships_for_node(current, "both", relationship_types):
                next_id = rel.target_id if rel.source_id == current else rel.source_id
                if next_id in seen:
                    continue
                seen.add(next_id)
                queue.append((next_id, path + [next_id], rel_path + [rel.id]))
        return [], []

    def traverse(
        self,
        start_id: str,
        direction: str = "out",
        relationship_types: set[str] | None = None,
        max_depth: int = 3,
    ) -> tuple[set[str], set[str]]:
        seen_nodes = {start_id}
        seen_rels: set[str] = set()
        queue: deque[tuple[str, int]] = deque([(start_id, 0)])
        while queue:
            current, depth = queue.popleft()
            if depth >= max_depth:
                continue
            for rel in self.relationships_for_node(current, direction, relationship_types):
                next_id = rel.target_id if rel.source_id == current else rel.source_id
                seen_rels.add(rel.id)
                if next_id not in seen_nodes:
                    seen_nodes.add(next_id)
                    queue.append((next_id, depth + 1))
        return seen_nodes, seen_rels

    def subgraph(self, node_ids: set[str], relationship_ids: set[str] | None = None) -> "InMemoryGraphRepository":
        sub = InMemoryGraphRepository()
        for node_id in node_ids:
            node = self.get_node(node_id)
            if node:
                sub.upsert_node(node)
        rels = [self.relationships[rel_id] for rel_id in relationship_ids] if relationship_ids else self.relationships.values()
        for rel in rels:
            if rel.source_id in sub.nodes and rel.target_id in sub.nodes:
                sub.upsert_relationship(rel)
        return sub

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodes": [node.model_dump() for node in sorted(self.nodes.values(), key=lambda item: item.id)],
            "relationships": [rel.model_dump() for rel in sorted(self.relationships.values(), key=lambda item: item.id)],
        }

    def save_json(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2, sort_keys=True), encoding="utf-8")

    @classmethod
    def load_json(cls, path: Path) -> "InMemoryGraphRepository":
        graph = cls()
        if not path.exists():
            return graph
        payload = json.loads(path.read_text(encoding="utf-8"))
        for node_data in payload.get("nodes", []):
            graph.upsert_node(GraphNode(**node_data))
        for rel_data in payload.get("relationships", []):
            graph.upsert_relationship(GraphRelationship(**rel_data))
        return graph
