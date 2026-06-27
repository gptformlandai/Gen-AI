# 07 Production Checklist

- Version graph definitions.
- Run compiler validation in CI.
- Review graph modeling reports for branching, cycles, and pattern coverage.
- Run path evals before graph releases.
- Store sessions in durable storage.
- Add auth and tenant isolation.
- Bound max steps and retry counts.
- Make tool calls typed and timeout-protected.
- Keep state snapshots for replay and debugging.
- Record trace IDs across tools and agents.
- Add human approval queues for risky actions.
- Monitor node-level success rate, path correctness, latency, and fallback rate.
