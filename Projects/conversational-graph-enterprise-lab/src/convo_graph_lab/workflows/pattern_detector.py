"""Detect conversational patterns from executed paths."""

from __future__ import annotations

from convo_graph_lab.workflows.sample_flows import CONVERSATIONAL_PATTERNS


def detect_patterns(path: list[str]) -> dict[str, bool]:
    return {
        name: _contains_ordered_subsequence(path, nodes)
        for name, nodes in CONVERSATIONAL_PATTERNS.items()
    }


def _contains_ordered_subsequence(path: list[str], pattern: list[str]) -> bool:
    position = 0
    for node_id in path:
        if position < len(pattern) and node_id == pattern[position]:
            position += 1
    return position == len(pattern)
