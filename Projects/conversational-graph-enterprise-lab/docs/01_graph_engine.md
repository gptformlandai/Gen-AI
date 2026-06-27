# 01 Graph Engine

## What It Covers

- Graph runner
- State store
- Context propagation
- Execution pointer
- Transition resolver
- Loop limits
- Error handling
- Interrupt/resume
- Exception handling
- State snapshots

## Code

- `graph_engine/runner.py`
- `graph_engine/state_store.py`
- `graph_engine/modeling.py`
- `transitions/conditions.py`
- `transitions/resolver.py`

## Run

```bash
convgraph-lab debug-conversation --input "Search docs for provider-search-service timeout"
convgraph-lab inspect-graph
```
