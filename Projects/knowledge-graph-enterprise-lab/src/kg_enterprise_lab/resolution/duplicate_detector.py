"""Duplicate detection using exact aliases and fuzzy names."""

from __future__ import annotations

from difflib import SequenceMatcher

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository


def normalize_name(value: str) -> str:
    return "".join(ch for ch in value.lower() if ch.isalnum())


def similarity(left: str, right: str) -> float:
    return SequenceMatcher(None, normalize_name(left), normalize_name(right)).ratio()


def detect_duplicates(graph: InMemoryGraphRepository, label: str = "Service", threshold: float = 0.86) -> list[tuple[str, str, float]]:
    nodes = graph.find_nodes(label=label)
    duplicates: list[tuple[str, str, float]] = []
    for index, left in enumerate(nodes):
        left_names = [left.name, *left.aliases]
        for right in nodes[index + 1 :]:
            right_names = [right.name, *right.aliases]
            score = max(similarity(a, b) for a in left_names for b in right_names)
            if score >= threshold:
                duplicates.append((left.id, right.id, round(score, 3)))
    return duplicates
