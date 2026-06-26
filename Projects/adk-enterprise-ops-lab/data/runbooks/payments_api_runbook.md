---
service: payments-api
domain: payments
severity_hint: sev1
owner: payments-platform
---

# Payments API High Latency Runbook

## Symptoms

- p95 latency exceeds 1200 ms.
- HTTP 500 or timeout rate rises after deployment.
- Database pool saturation or payment gateway timeout appears in logs.

## Investigation

1. Check service health.
2. Inspect recent deployments.
3. Compare error rate before and after deploy.
4. Check database latency and payment gateway dependency status.
5. Confirm whether retries are amplifying load.

## Remediation

- Roll back the latest deployment if latency started immediately after release.
- Increase database connection pool only after confirming saturation.
- Disable non-critical fraud enrichment if gateway latency is the bottleneck.
- Escalate to payments on-call for customer-impacting checkout failures.

## Verification

- p95 latency below 600 ms.
- Error rate below 1 percent.
- Successful payment authorization rate returns to baseline.

