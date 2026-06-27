# 03 Memory, Tools, And Agents

## Memory

The lab includes short-term session memory, long-term memory, relevance retrieval, pruning, context compression, and slot filling.

## Tools

Mock tools:

- `search_tool`
- `incident_lookup_tool`
- `user_profile_tool`
- `graph_query_tool`

Each tool has a `ToolSpec` with required and optional arguments. Missing required inputs fail before the handler runs, which makes tool failures predictable and traceable.

## Agents

Specialists:

- routing
- clarification
- support
- incident
- developer
- tool
- summary
- coordinator

## Code

- `memory/memory_store.py`
- `tools/registry.py`
- `agents/agent_registry.py`
