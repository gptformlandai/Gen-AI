# Debug Memo: Slow Or Expensive Path

## Scenario

The slow path is a production change with a simulated slow risk-assessment tool:

```bash
mcp-change run \
  --summary "Deploy production release with slow dependency scan" \
  --environment production \
  --approved \
  --simulate-slow-risk-ms 250
```

## Observation

The risk-assessment tool dominates end-to-end latency because all later decisions depend on risk classification. Even though the workflow is local, this models a common production issue: a dependency scanner, policy engine, or security tool blocks the critical path.

## Why It Matters

Risk scoring is useful, but if it sits synchronously in front of every change ticket, p95 latency can climb quickly. This can make operators bypass the workflow during incidents.

## Mitigations

- Cache risk results for identical change summaries.
- Run slow enrichment asynchronously after a cheap initial policy check.
- Split risk scoring into fast required checks and slow advisory checks.
- For emergency changes, allow a break-glass path that records approval and runs slow checks after ticket creation.

## Remaining Risk

Caching must include environment and requester. A staging risk score must not be reused for production.
