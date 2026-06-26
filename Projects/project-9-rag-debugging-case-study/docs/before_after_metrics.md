# Before-Vs-After Metrics

| Metric | Baseline | Improved | Delta |
|---|---:|---:|---:|
| Pass rate | 58.33% | 100.00% | +41.67% |
| Top-1 document accuracy | 58.33% | 100.00% | +41.67% |
| Top-3 document recall | 100.00% | 100.00% | +0.00% |
| Expected term coverage | 54.55% | 100.00% | +45.45% |

## Failure Counts

| Failure layer | Baseline | Improved |
|---|---:|---:|
| retrieval | 5 | 0 |

## Row Results

| Question | Category | Baseline pass | Improved pass | Baseline doc | Improved doc |
|---|---|---:|---:|---|---|
| q001 | direct_match | True | True | password_reset | password_reset |
| q002 | title_intent | True | True | analytics_export | analytics_export |
| q003 | synonym_gap | False | True | admin_permissions | incident_response |
| q004 | morphology_and_synonym | False | True | api_errors | webhook_delivery |
| q005 | synonym_gap | False | True | account_access | data_deletion |
| q006 | direct_match | False | True | password_reset | sso_setup |
| q007 | direct_match | True | True | cache_ttl | cache_ttl |
| q008 | synonym_gap | False | True | api_errors | rate_limits |
| q009 | direct_match | True | True | refunds | refunds |
| q010 | direct_match | True | True | audit_export | audit_export |
| q011 | direct_match | True | True | mobile_offline | mobile_offline |
| q012 | multi_sentence | True | True | sso_setup | sso_setup |
