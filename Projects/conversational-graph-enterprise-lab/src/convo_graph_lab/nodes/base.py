"""Base node contract."""

from __future__ import annotations

from convo_graph_lab.schema.models import ConversationState, NodeDefinition, NodeResult, NodeStatus


class BaseNode:
    node_type = "BaseNode"

    def __init__(self, definition: NodeDefinition) -> None:
        self.definition = definition

    def run(self, state: ConversationState, services: object) -> NodeResult:
        return NodeResult(node_id=self.definition.id, status=NodeStatus.SUCCESS)

    def config(self, key: str, default: object = None) -> object:
        return self.definition.config.get(key, default)
