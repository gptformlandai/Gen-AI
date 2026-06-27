# 04 DSL And Compilation

The graph DSL is JSON and supports nodes, edges, conditions, and metadata.

Compiler validation checks:

- missing start node
- unknown node type
- invalid node configuration
- missing edge source/target
- unreachable nodes
- cycles

The graph modeling report also summarizes terminal nodes, branching nodes, node type counts, cycle presence, and conversational pattern coverage.

## Code

- `data/sample_graphs/enterprise_orchestrator.json`
- `graph_engine/compiler.py`
- `graph_engine/validator.py`
