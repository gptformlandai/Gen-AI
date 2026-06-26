# Tool Governance

## Categories

- Read-only tools: RAG, service health, deployments, error rate, on-call lookup.
- Write tools: artifact save, memory add.
- Production-changing tools: rollback, scale, cancel query placeholders.

## Policy

- Read-only tools may run automatically.
- Write tools must record audit metadata.
- Production-changing tools require human approval.

## Registry

`tools/tool_registry.py` is the source of tool metadata.

