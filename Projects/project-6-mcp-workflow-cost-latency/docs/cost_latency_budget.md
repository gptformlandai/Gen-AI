# Cost And Latency Budget Sheet

## Budget Assumptions

This project runs locally, so no real model/API billing occurs. We still estimate budget as if each MCP boundary call had operational cost.

| Unit | Assumption |
|---|---:|
| Resource read | 1 request |
| Tool call | 1 request |
| Token estimate | approximately 1.3 tokens per word |
| Estimated cost | `$0.000002` per estimated token |
| Latency budget | 500 ms end-to-end for normal path |
| Request budget | 4 MCP requests for approved path |

## Normal Low-Risk Path

Expected calls:

1. Read policy resource.
2. Call risk assessment tool.
3. Call ticket creation tool.
4. Call notification tool.

Expected result:

- 4 MCP requests
- below 500 ms locally
- no approval delay

## High-Risk Pending Path

Expected calls:

1. Read policy resource.
2. Call risk assessment tool.

Expected result:

- 2 MCP requests
- stops before ticket creation
- saves cost and avoids unsafe action

## Approved High-Risk Path

Expected calls:

1. Read policy resource.
2. Call risk assessment tool.
3. Call ticket creation tool with approval.
4. Call notification tool.

Expected result:

- 4 MCP requests
- higher review latency outside the automated workflow
- dangerous action is gated
