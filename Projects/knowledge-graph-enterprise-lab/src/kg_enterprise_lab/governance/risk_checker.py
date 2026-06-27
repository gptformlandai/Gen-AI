"""Risk checks for expensive or unsafe traversals."""

from __future__ import annotations


def check_traversal_depth(depth: int, max_allowed: int = 5) -> list[str]:
    if depth > max_allowed:
        return [f"Traversal depth {depth} exceeds max allowed {max_allowed}."]
    return []


def check_result_size(size: int, max_allowed: int = 500) -> list[str]:
    if size > max_allowed:
        return [f"Result size {size} exceeds max allowed {max_allowed}."]
    return []
