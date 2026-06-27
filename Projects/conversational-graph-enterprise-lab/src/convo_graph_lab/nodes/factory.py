"""Node factory for graph runtime."""

from __future__ import annotations

from convo_graph_lab.nodes.base import BaseNode
from convo_graph_lab.nodes.node_types import (
    AgentNode,
    DecisionNode,
    EndNode,
    FallbackNode,
    HumanApprovalNode,
    InputNode,
    LLMNode,
    MemoryNode,
    RetryNode,
    RouterNode,
    ToolNode,
    ValidationNode,
    WorkflowNode,
)
from convo_graph_lab.schema.models import NodeDefinition


class NodeFactory:
    registry: dict[str, type[BaseNode]] = {
        "InputNode": InputNode,
        "LLMNode": LLMNode,
        "ToolNode": ToolNode,
        "DecisionNode": DecisionNode,
        "RouterNode": RouterNode,
        "MemoryNode": MemoryNode,
        "ValidationNode": ValidationNode,
        "WorkflowNode": WorkflowNode,
        "AgentNode": AgentNode,
        "HumanApprovalNode": HumanApprovalNode,
        "FallbackNode": FallbackNode,
        "RetryNode": RetryNode,
        "EndNode": EndNode,
    }

    def create(self, definition: NodeDefinition) -> BaseNode:
        node_cls = self.registry.get(definition.type)
        if not node_cls:
            raise ValueError(f"Unknown node type: {definition.type}")
        return node_cls(definition)
