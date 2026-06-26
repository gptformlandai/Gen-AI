---
service: search-service
domain: search
severity_hint: sev2
owner: search-platform
---

# Search Service Errors Runbook

## Symptoms

- Search API returns elevated 5xx responses.
- Query latency increases after index refresh.
- Users report missing or stale search results.

## Investigation

1. Check search-service health and error rate.
2. Verify index refresh status.
3. Compare recent deploys and schema migrations.
4. Inspect query cache hit rate.
5. Check shard allocation and hot partitions.

## Remediation

- Pause index refresh if shard pressure is high.
- Revert schema change if errors started after migration.
- Clear only the affected query cache namespace.
- Escalate to search on-call if customer-facing error rate exceeds 5 percent.

## Verification

- 5xx rate below 1 percent.
- p95 query latency below 800 ms.
- Index freshness within service-level objective.

