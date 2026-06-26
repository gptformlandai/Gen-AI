# Baseline vs Advanced RAG Comparison

- Total questions: 25
- Baseline passed: 19 (76.00%)
- Advanced passed: 25 (100.00%)
- Improved failures: 6

| Question | Role | Expected | Baseline | Advanced | Improved | Baseline category | Advanced category |
|---|---|---|---:|---:|---:|---|---|
| eval-001 | employee | answered | True | True | False | pass | pass |
| eval-002 | manager | answered | True | True | False | pass | pass |
| eval-003 | support_lead | answered | True | True | False | pass | pass |
| eval-004 | operator | answered | True | True | False | pass | pass |
| eval-005 | employee | answered | True | True | False | pass | pass |
| eval-006 | analyst | answered | True | True | False | pass | pass |
| eval-007 | admin | answered | True | True | False | pass | pass |
| eval-008 | hr | answered | True | True | False | pass | pass |
| eval-009 | analyst | answered | False | True | True | missed_retrieval | pass |
| eval-010 | auditor | answered | True | True | False | pass | pass |
| eval-011 | operator | answered | False | True | True | missed_retrieval | pass |
| eval-012 | agent | answered | True | True | False | pass | pass |
| eval-013 | manager | answered | True | True | False | pass | pass |
| eval-014 | employee | answered | True | True | False | pass | pass |
| eval-015 | support_lead | answered | True | True | False | pass | pass |
| eval-016 | operator | answered | True | True | False | pass | pass |
| eval-017 | employee | answered | True | True | False | pass | pass |
| eval-018 | admin | answered | True | True | False | pass | pass |
| eval-019 | employee | refused | False | True | True | expected_refusal_failed | pass |
| eval-020 | employee | refused | False | True | True | expected_refusal_failed | pass |
| eval-021 | employee | refused | True | True | False | pass | pass |
| eval-022 | employee | refused | True | True | False | pass | pass |
| eval-023 | employee | refused | False | True | True | expected_refusal_failed | pass |
| eval-024 | employee | refused | False | True | True | expected_refusal_failed | pass |
| eval-025 | auditor | answered | True | True | False | pass | pass |

## Before-vs-After Notes

- `eval-009` improves because query rewriting adds terms from the report export document.
- `eval-011` improves because incident-triage rewriting and reranking boost the incident runbook.
- `eval-023` and `eval-024` show permission-aware refusal for employee access to audit/admin details.
