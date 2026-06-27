"""BFS and DFS traversals."""

from __future__ import annotations

from collections import deque

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository


def bfs(graph: InMemoryGraphRepository, start_id: str, max_depth: int = 3) -> list[str]:
    seen = {start_id}
    order: list[str] = []
    queue: deque[tuple[str, int]] = deque([(start_id, 0)])
    while queue:
        node_id, depth = queue.popleft()
        order.append(node_id)
        if depth >= max_depth:
            continue
        for neighbor in graph.neighbors(node_id):
            if neighbor.id not in seen:
                seen.add(neighbor.id)
                queue.append((neighbor.id, depth + 1))
    return order


def dfs(graph: InMemoryGraphRepository, start_id: str, max_depth: int = 3) -> list[str]:
    order: list[str] = []
    seen: set[str] = set()

    def visit(node_id: str, depth: int) -> None:
        if node_id in seen or depth > max_depth:
            return
        seen.add(node_id)
        order.append(node_id)
        for neighbor in graph.neighbors(node_id):
            visit(neighbor.id, depth + 1)

    visit(start_id, 0)
    return order
