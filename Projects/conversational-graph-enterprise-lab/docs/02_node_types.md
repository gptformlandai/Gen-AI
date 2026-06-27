# 02 Node Types

Implemented node types:

- InputNode
- LLMNode
- ToolNode
- DecisionNode
- RouterNode
- MemoryNode
- ValidationNode
- WorkflowNode
- AgentNode
- HumanApprovalNode
- FallbackNode
- RetryNode
- EndNode

Each node accepts `ConversationState`, updates structured context, and returns `NodeResult`.

## Code

`nodes/node_types.py`
