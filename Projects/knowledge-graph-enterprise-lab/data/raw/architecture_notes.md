# Enterprise Architecture Notes

The mobile-app calls provider-search-service for provider discovery and payments-api for member payments.
Provider search reads provider-db tables providers, provider_locations, and provider_contracts.
Provider search consumes kafka-topic-provider-directory-updates and publishes kafka-topic-provider-search-events.
Incident INC-1001 showed database timeout and Provider Search API 504 responses after a provider directory import.
Runbook Provider Search Latency recommends checking provider-db locks, topic lag, and cache warmup.

Payments API consumes kafka-topic-user-request-events, writes payment ledger data, publishes kafka-topic-payment-events, and calls notification-service.
Incident INC-1002 happened when notification callback retries exhausted the payments-api connection pool.

Claims orchestrator calls eligibility-api and payments-api, reads and writes claims, and publishes kafka-topic-claim-events.
Eligibility API reads member eligibility data and can return stale cache responses when invalidation is delayed.
