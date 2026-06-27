# 05 Observability And Evaluation

## Observability

Each node emits a trace event with:

- node ID and type
- status
- selected edge
- next node
- state snapshot
- state snapshot ID
- output/error
- latency

Metrics track node execution counts and latency.

`debug-conversation` builds a report with selected transitions, failures, slow nodes, state snapshots, and detected conversational patterns.

## Evaluation

Eval cases check:

- conversation success
- expected path correctness
- slot filling
- multi-turn behavior
- tool path usage

## Run

```bash
convgraph-lab run-evals
```
