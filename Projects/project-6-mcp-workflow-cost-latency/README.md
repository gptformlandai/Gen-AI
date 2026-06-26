# Project 6: MCP-Enabled Workflow With Cost And Latency Budget

This project implements an MCP-enabled change-management workflow.

The workflow consumes MCP-exposed capabilities through a local gateway:

- an MCP resource: `policy://change-management`
- an MCP tool: `risk.assess_change`
- an MCP tool: `ticket.create_change`
- an MCP tool: `notify.stakeholders`

The workflow reads policy, assesses risk, gates risky production changes behind human approval, creates a change ticket when allowed, and records request, token, cost, and latency budget estimates.

## Project Requirements Coverage

| Spec requirement | How this project handles it |
|---|---|
| At least one MCP tool or resource | `mcp_gateway.py` exposes one resource and three tools. |
| Workflow meaningfully uses MCP | `workflow.py` only interacts with policy/risk/ticket capabilities through the gateway boundary. |
| Approval or policy boundary | Production/high-risk changes stop at `pending_approval` unless `--approved` is provided. |
| Token, latency, or request budget | `budget.py` estimates tokens, request count, cost, and latency; runtime records measured latency. |
| Debug memo | `docs/debug_memo_slow_path.md` describes the expensive/slow path. |

## Architecture

```text
change request
    |
    v
read MCP resource: policy://change-management
    |
    v
call MCP tool: risk.assess_change
    |
    v
policy gate
    |-- high risk + no approval --> pending_approval
    |
    v
call MCP tool: ticket.create_change
    |
    v
call MCP tool: notify.stakeholders
    |
    v
final result + budget + trace
```

## Why A Local MCP Gateway

This project keeps the MCP boundary local and deterministic so it can be tested without external credentials. The important learning point is the boundary:

- the workflow discovers and calls named capabilities;
- tools and resources have structured contracts;
- risky tool calls are policy-gated;
- budget and latency are measured around capability calls.

A production version would replace the in-process gateway with a real MCP client connected to remote MCP servers.

## Run Locally

```bash
cd Projects/project-6-mcp-workflow-cost-latency
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Low-risk staging change:

```bash
mcp-change run \
  --summary "Restart the staging support dashboard worker" \
  --environment staging \
  --requester ops@example.com \
  --output docs/demo_low_risk.json
```

Production high-risk change without approval:

```bash
mcp-change run \
  --summary "Delete stale production records after export" \
  --environment production \
  --requester ops@example.com \
  --output docs/demo_pending_approval.json
```

Production high-risk change with approval:

```bash
mcp-change run \
  --summary "Delete stale production records after export" \
  --environment production \
  --requester ops@example.com \
  --approved \
  --output docs/demo_approved.json
```

Slow-path debug run:

```bash
mcp-change run \
  --summary "Deploy production release with slow dependency scan" \
  --environment production \
  --requester ops@example.com \
  --approved \
  --simulate-slow-risk-ms 250
```

## Tests

```bash
pytest
```

The tests verify MCP resource access, MCP tool calls, approval gating, budget accounting, and slow-path latency capture.
