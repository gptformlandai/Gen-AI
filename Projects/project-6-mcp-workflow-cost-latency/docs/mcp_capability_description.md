# MCP Capability Description

Project 6 exposes a local MCP gateway with one resource and three tools.

## Resources

### `policy://change-management`

Provides change-management policy text and structured thresholds.

Fields:

- production changes require approval;
- destructive actions require approval;
- low-risk staging changes can proceed automatically;
- emergency changes require notification.

## Tools

### `risk.assess_change`

Input:

- `summary`
- `environment`
- `requester`

Output:

- `risk_level`
- `approval_required`
- `reasons`

Meaningful use: the workflow uses this result to decide whether to stop for approval or continue.

### `ticket.create_change`

Input:

- `summary`
- `environment`
- `requester`
- `risk_level`
- `approved`

Output:

- `ticket_id`
- `created`
- `message`

Meaningful use: this is the risky action. Production/high-risk changes cannot call this tool successfully unless approval is present.

### `notify.stakeholders`

Input:

- `ticket_id`
- `environment`
- `risk_level`

Output:

- notification status

Meaningful use: production and emergency changes must notify stakeholders after ticket creation.
