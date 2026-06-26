# State Transition Notes

## Main Happy Path

1. `receive_request` stores the request and initializes counters.
2. `classify_request` assigns category and risk.
3. `lookup_policy` calls the policy tool.
4. `draft_plan` creates an implementation plan.
5. `execute_action` runs automatically for low-risk requests.
6. `finalize` emits the final workflow result.

## Human Approval Path

High-risk categories such as admin access, production deletion, or production deployment set `approval_required=true`.

- If `human_decision` is missing, the workflow stops with `pending_human_approval`.
- If `human_decision=rejected`, the workflow stops with `rejected`.
- If `human_decision=approved`, the workflow executes the action.

This is meaningful because high-risk requests cannot reach `execute_action` without approval.

## Retry And Recovery Path

`lookup_policy` retries transient tool failures until `max_policy_retries` is reached. If the tool still fails, the graph routes to `recover_policy`, which applies a conservative fallback policy:

- require human approval;
- limit execution scope;
- assign to manual operations review if needed.

## Why LangGraph Here

The point is not just "agents." The point is explicit state and inspectable routing:

- every node has a named responsibility;
- every decision is visible;
- failure handling is part of the graph instead of hidden in ad hoc code.
