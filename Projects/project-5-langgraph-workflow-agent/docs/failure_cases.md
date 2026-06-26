# Failure Cases

| Failure | Where it appears | System behavior |
|---|---|---|
| Policy tool transient failure | `lookup_policy` | Retry once before continuing. |
| Policy tool persistent failure | `lookup_policy` -> `recover_policy` | Use fallback conservative policy and require human approval. |
| High-risk request without approval | `human_approval` | Stop with `pending_human_approval`; do not execute. |
| Human rejects plan | `human_approval` | Stop with `rejected`; do not execute. |
| Bad or ambiguous input | `classify_request` | Route to manual-review category with medium risk. |
| Execution receives unapproved high-risk plan | `execute_action` | Return blocked result instead of executing. |

## Example Bad Tool Output

The policy tool can be configured to fail for the first N attempts. This makes the retry and recovery path testable without relying on real outages.
