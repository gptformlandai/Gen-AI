---
service: kafka-consumers
domain: streaming
severity_hint: sev2
owner: data-platform
---

# Kafka Consumer Lag Runbook

## Symptoms

- Consumer lag grows for more than 10 minutes.
- Downstream projections become stale.
- Consumer rebalance loops appear in logs.

## Investigation

1. Check consumer group lag by partition.
2. Verify broker health.
3. Inspect recent deployments for consumer config changes.
4. Check poison-message retries and dead-letter queue volume.
5. Compare partition count with active consumer count.

## Remediation

- Increase consumer partitions or replicas when capacity is the bottleneck.
- Stop poison-message retry loops and move bad events to the dead-letter queue.
- Roll back consumer config changes that reduce max poll records too aggressively.
- Escalate to data-platform on-call when lag affects customer-visible data.

## Verification

- Lag decreases for three consecutive checks.
- No rebalance loop in the last 10 minutes.
- Projection freshness recovers.

