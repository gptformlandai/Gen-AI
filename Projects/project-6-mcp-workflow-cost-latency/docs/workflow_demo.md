# Workflow Demo

Project 6 includes four generated workflow runs.

| Demo | Status | MCP requests | What it proves |
|---|---|---:|---|
| `demo_low_risk.json` | `completed` | 4 | Low-risk staging change can proceed automatically. |
| `demo_pending_approval.json` | `pending_approval` | 2 | High-risk production deletion stops before ticket creation. |
| `demo_approved.json` | `completed` | 4 | Approved high-risk production change can create a ticket. |
| `demo_slow_path.json` | `completed` | 4 | Slow risk tool dominates latency and is visible in trace. |

## How To Read The Trace

Every run records:

- `mcp.resource.read` for policy loading;
- `mcp.tool.risk` for risk assessment;
- `approval.gate` when the workflow blocks a risky action;
- `mcp.tool.ticket` when ticket creation is allowed;
- `mcp.tool.notify` for stakeholder notification.

## Budget Observation

The pending-approval path uses only two MCP requests because it stops before the risky ticket tool. This is both safer and cheaper. The approved path uses four MCP requests because it reads policy, assesses risk, creates the ticket, and sends notification.
