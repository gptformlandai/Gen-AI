# Production Notes

## State

Replace `InMemoryStateStore` with Redis, Postgres, or a workflow runtime. Persist execution pointer, slots, retry counts, trace ID, and interruption state.

## Tools

Wrap tools with auth, timeouts, retries, idempotency keys, and typed contracts.

## Agents

Replace deterministic agents with LLM-backed agents behind schemas. Keep routing decisions and confidence scores observable.

## Observability

Export traces to OpenTelemetry. Track node success rate, fallback rate, tool failure rate, resume rate, and path correctness.

## Release Safety

Run graph compiler validation and evals before deploying graph changes.
