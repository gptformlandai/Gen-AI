# Callbacks

## What It Is

Lifecycle hooks record before/after agent calls, before/after tool calls, errors, safety outcomes, request IDs, session IDs, latency, and outcomes.

## Where It Appears

- `callbacks/lifecycle_callbacks.py`
- `runner.py`
- `.traces/*.jsonl`

## Why It Matters

Callbacks let you add observability and guardrails without mixing logging code into every agent.

## Extend It

Export callback events to OpenTelemetry or Cloud Trace.

