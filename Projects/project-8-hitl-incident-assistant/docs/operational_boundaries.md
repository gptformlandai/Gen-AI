# Operational Boundaries

## System Role

The assistant is allowed to triage incident reports, propose remediation actions, run safe simulated diagnostics, persist state, and resume after a human decision.

It is not allowed to perform irreversible or customer-visible actions without approval.

## Safe Actions

Safe actions can run immediately:

- collect diagnostics;
- notify the on-call owner;
- open an incident channel.

These actions are observational or communicative. They should not change production behavior.

## Approval-Required Actions

The assistant must pause before:

- rolling back a deployment;
- restarting a service;
- scaling capacity;
- posting a status-page update.

These actions are gated because they can affect availability, cost, customer communication, or data integrity.

## Clarification Boundary

The assistant must ask for clarification when the report does not identify:

- affected service;
- user or business impact;
- observable signal such as latency, error rate, queue depth, or alert name.

## Latency Boundary

The workflow tracks estimated action latency against a 1500 ms budget. If a proposed action plan exceeds the budget, the assistant records a warning event so the incident commander can simplify the path or split work.

## Human Escalation Rules

Escalate to a human when:

- the report is ambiguous;
- a state-changing action is required;
- customer-facing communication is proposed;
- action latency exceeds the budget;
- the human rejects a proposed remediation and another path is needed.

