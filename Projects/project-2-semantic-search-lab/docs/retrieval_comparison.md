# Retrieval Comparison

- Total queries: 12
- Exact hit rate @5: 100.00%
- ANN hit rate @5: 100.00%

| Query | Filters | Exact hit | ANN hit | Exact top topic | ANN top topic |
|---|---|---:|---:|---|---|
| q001 | product=identity | True | True | password_reset | password_reset |
| q002 | product=procurement | True | True | vendor_onboarding | vendor_onboarding |
| q003 | product=support | True | True | support_dashboard | support_dashboard |
| q004 | product=healthcare | True | True | appointment_reminders | appointment_reminders |
| q005 | product=knowledge_base | True | True | knowledge_review | knowledge_review |
| q006 | product=finance | True | True | csv_reconciliation | csv_reconciliation |
| q007 | product=admin | True | True | role_based_access | role_based_access |
| q008 | product=hr | True | True | new_hire_onboarding | new_hire_onboarding |
| q009 | doc_type=reference | True | True | report_exports | report_exports |
| q010 | doc_type=policy | True | True | audit_trail | audit_trail |
| q011 | audience=employees | True | True | knowledge_review | knowledge_review |
| q012 | none | True | True | vendor_onboarding | vendor_onboarding |

## Top Result Differences

| Query | Exact top chunk | Exact score | ANN top chunk | ANN score | Same top chunk |
|---|---|---:|---|---:|---:|
| q001 | `password_reset-001-global::chunk-000` | 0.497 | `password_reset-001-global::chunk-000` | 0.497 | True |
| q002 | `vendor_onboarding-003-us::chunk-000` | 0.295 | `vendor_onboarding-003-us::chunk-000` | 0.295 | True |
| q003 | `support_dashboard-001-eu::chunk-000` | 0.647 | `support_dashboard-003-eu::chunk-000` | 0.627 | False |
| q004 | `appointment_reminders-005-apac::chunk-000` | 0.490 | `appointment_reminders-005-apac::chunk-000` | 0.490 | True |
| q005 | `knowledge_review-002-global::chunk-000` | 0.338 | `knowledge_review-002-global::chunk-000` | 0.338 | True |
| q006 | `csv_reconciliation-001-us::chunk-000` | 0.694 | `csv_reconciliation-001-us::chunk-000` | 0.694 | True |
| q007 | `role_based_access-002-eu::chunk-000` | 0.770 | `role_based_access-002-eu::chunk-000` | 0.770 | True |
| q008 | `new_hire_onboarding-003-apac::chunk-000` | 0.110 | `new_hire_onboarding-003-apac::chunk-000` | 0.110 | True |
| q009 | `report_exports-002-global::chunk-000` | 0.557 | `report_exports-002-global::chunk-000` | 0.557 | True |
| q010 | `audit_trail-001-us::chunk-000` | 0.510 | `audit_trail-002-us::chunk-000` | 0.478 | False |
| q011 | `knowledge_review-002-global::chunk-000` | 0.523 | `knowledge_review-002-global::chunk-000` | 0.523 | True |
| q012 | `vendor_onboarding-003-us::chunk-000` | 0.146 | `vendor_onboarding-003-us::chunk-000` | 0.146 | True |

## Notes

- Exact search is the quality baseline because it evaluates every filtered chunk.
- ANN search may return a different top topic because LSH only scores bucket candidates.
- A failed filtered query can mean the filter removed the relevant document, not that embeddings failed.
