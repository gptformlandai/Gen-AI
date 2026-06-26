# Failure Log

## Latency Failures

Failure: the assistant proposes too many actions during an active incident.

User-visible impact: responders wait for a slow workflow while the system is already degraded.

Mitigation: every action has estimated latency and the workflow records a `latency_budget_exceeded` event when the total estimate crosses the budget.

## Ambiguity Failures

Failure: the incident report says something like "the app is weird" without service, impact, or signals.

User-visible impact: the assistant may classify severity incorrectly or propose the wrong remediation.

Mitigation: incomplete reports stop in `needs_clarification` with concrete follow-up questions.

## Unsafe Action Failures

Failure: an assistant restarts production, rolls back a deploy, scales capacity, or updates a status page without approval.

User-visible impact: avoidable downtime, higher cost, data risk, or incorrect customer communication.

Mitigation: those actions are represented as pending `approval_required` actions and cannot execute until a human decision is recorded.

## Long-Horizon Failures

Failure: workflow state is lost between triage and approval.

User-visible impact: a human cannot tell what was proposed, approved, rejected, or executed.

Mitigation: each incident has a persisted JSON state with an event log and action-level approval status.

