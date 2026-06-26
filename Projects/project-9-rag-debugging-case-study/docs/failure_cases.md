# Failure Cases

This file keeps the failed baseline rows visible so the improvement is traceable.

| Question | Category | Expected doc | Baseline doc | Failure layer | Missing terms | Improved pass |
|---|---|---|---|---|---|---:|
| q003 | synonym_gap | incident_response | admin_permissions | retrieval | severity, incident commander, mitigation | True |
| q004 | morphology_and_synonym | webhook_delivery | api_errors | retrieval | exponential backoff, HMAC signature, 24 hours | True |
| q005 | synonym_gap | data_deletion | account_access | retrieval | 30 day, deletion, legal hold | True |
| q006 | direct_match | sso_setup | password_reset | retrieval | SAML, OIDC, domain verification | True |
| q008 | synonym_gap | rate_limits | api_errors | retrieval | HTTP 429, Retry-After, 600 requests | True |
