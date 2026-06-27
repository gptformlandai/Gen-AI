"""Graph compiler validation checks."""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass

from convo_graph_lab.schema.models import GraphDefinition


VALID_NODE_TYPES = {
    "InputNode",
    "LLMNode",
    "ToolNode",
    "DecisionNode",
    "RouterNode",
    "MemoryNode",
    "ValidationNode",
    "WorkflowNode",
    "AgentNode",
    "HumanApprovalNode",
    "FallbackNode",
    "RetryNode",
    "EndNode",
}


@dataclass(frozen=True)
class GraphValidationIssue:
    severity: str
    code: str
    message: str


def validate_graph_definition(definition: GraphDefinition) -> list[GraphValidationIssue]:
    issues: list[GraphValidationIssue] = []
    node_ids = {node.id for node in definition.nodes}
    if definition.start_node_id not in node_ids:
        issues.append(GraphValidationIssue("error", "missing_start", "Start node does not exist."))
    for node in definition.nodes:
        if node.type not in VALID_NODE_TYPES:
            issues.append(GraphValidationIssue("error", "unknown_node_type", f"Unknown node type {node.type} for {node.id}."))
        issues.extend(_validate_node_config(node, node_ids))
    for edge in definition.edges:
        if edge.source not in node_ids:
            issues.append(GraphValidationIssue("error", "missing_edge_source", f"Edge {edge.id} source is missing."))
        if edge.target not in node_ids:
            issues.append(GraphValidationIssue("error", "missing_edge_target", f"Edge {edge.id} target is missing."))
    unreachable = sorted(node_ids - _reachable_nodes(definition))
    for node_id in unreachable:
        issues.append(GraphValidationIssue("warning", "unreachable_node", f"Node {node_id} is unreachable."))
    if _has_cycle(definition):
        issues.append(GraphValidationIssue("info", "cycle_detected", "Graph contains at least one cycle; ensure loop limits are configured."))
    return issues


def _validate_node_config(node, node_ids: set[str]) -> list[GraphValidationIssue]:
    issues: list[GraphValidationIssue] = []
    if node.type == "ToolNode" and not node.config.get("tool"):
        issues.append(GraphValidationIssue("error", "missing_tool_config", f"ToolNode {node.id} requires config.tool."))
    if node.type == "RouterNode" and not isinstance(node.config.get("routes"), dict):
        issues.append(GraphValidationIssue("error", "missing_routes_config", f"RouterNode {node.id} requires config.routes."))
    if node.type == "RetryNode":
        target = node.config.get("target_node_id")
        if not target:
            issues.append(GraphValidationIssue("error", "missing_retry_target", f"RetryNode {node.id} requires config.target_node_id."))
        elif target not in node_ids:
            issues.append(GraphValidationIssue("error", "invalid_retry_target", f"RetryNode {node.id} target {target} does not exist."))
    if node.type == "AgentNode" and not node.config.get("agent"):
        issues.append(GraphValidationIssue("warning", "missing_agent_config", f"AgentNode {node.id} will use coordinator fallback."))
    return issues


def _reachable_nodes(definition: GraphDefinition) -> set[str]:
    outgoing: dict[str, list[str]] = defaultdict(list)
    for edge in definition.edges:
        outgoing[edge.source].append(edge.target)
    seen = {definition.start_node_id}
    queue: deque[str] = deque([definition.start_node_id])
    while queue:
        node_id = queue.popleft()
        for target in outgoing.get(node_id, []):
            if target not in seen:
                seen.add(target)
                queue.append(target)
    return seen


def _has_cycle(definition: GraphDefinition) -> bool:
    outgoing: dict[str, list[str]] = defaultdict(list)
    for edge in definition.edges:
        outgoing[edge.source].append(edge.target)
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node_id: str) -> bool:
        if node_id in visiting:
            return True
        if node_id in visited:
            return False
        visiting.add(node_id)
        for target in outgoing.get(node_id, []):
            if visit(target):
                return True
        visiting.remove(node_id)
        visited.add(node_id)
        return False

    return any(visit(node.id) for node in definition.nodes)
