---
service: shared-postgres
domain: database
severity_hint: sev1
owner: database-reliability
---

# Database Latency Runbook

## Symptoms

- Query latency exceeds 1000 ms.
- Lock wait time rises.
- Application pools show connection starvation.

## Investigation

1. Check database health and current lock waits.
2. Inspect top slow queries.
3. Compare traffic spike and deployment timelines.
4. Check connection pool usage by service.
5. Identify long-running transactions.

## Remediation

- Cancel runaway analytical query after approval.
- Scale read replicas for read-heavy load.
- Reduce application pool size if one service is starving others.
- Escalate to database on-call for customer-impacting write latency.

## Verification

- p95 query latency below 500 ms.
- Lock waits return to normal.
- Application error rate recovers.

