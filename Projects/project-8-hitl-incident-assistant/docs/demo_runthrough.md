# Demo Run-Through

This run shows a long-lived incident workflow that pauses before unsafe production actions, resumes after approval, and closes after a human observation.

| Step | Status | Boundary | Pending actions | Executed actions |
|---|---|---|---|---|
| 1 | waiting_for_human | State-changing or customer-visible actions require human approval. | rollback_deploy, post_status_page_update | collect_diagnostics, notify_oncall, open_incident_channel |
| 2 | monitoring | All pending approval decisions have been recorded. | none | collect_diagnostics, notify_oncall, open_incident_channel, rollback_deploy, post_status_page_update |
| 3 | resolved | Human observation marked the incident stable or resolved. | none | collect_diagnostics, notify_oncall, open_incident_channel, rollback_deploy, post_status_page_update |

## Event Log

- `incident_started`: Incident workflow started.
- `safe_action_executed`: Executed safe action: collect_diagnostics.
- `safe_action_executed`: Executed safe action: notify_oncall.
- `safe_action_executed`: Executed safe action: open_incident_channel.
- `approval_gate`: State-changing or customer-visible actions require human approval.
- `unsafe_action_approved`: incident-commander@example.com approved and executed: rollback_deploy.
- `unsafe_action_approved`: incident-commander@example.com approved and executed: post_status_page_update.
- `monitoring_started`: Workflow resumed into monitoring.
- `observation_recorded`: Checkout metrics are stable and the incident is resolved.
- `incident_resolved`: Incident marked resolved from follow-up observation.
