# 17 Observability

## What It Is

Observability records structured logs, trace IDs, metrics, query logs, ingestion logs, graph mutation logs, and GraphRAG decision traces.

## Why It Matters

When an answer is wrong, you need to inspect ingestion, entity linking, retrieval, and generation decisions.

## Where It Appears

- `observability/logger.py`
- `observability/tracing.py`
- `observability/metrics.py`
- `schemas/graphrag.py`

## How To Run

```bash
kg-lab run-graphrag --question "Use GraphRAG to explain why provider-search-service may be slow."
```

GraphRAG records request and grounding counters in the response trace so local runs expose retrieval decisions and basic metrics.

## How To Extend

Send logs and spans to OpenTelemetry, emit latency histograms, and connect GraphRAG traces to evaluation dashboards.

## Common Mistakes

- Logging only the final answer.
- Dropping trace IDs between API, retrieval, and graph mutation.
- Not tracking confidence and source refs.
