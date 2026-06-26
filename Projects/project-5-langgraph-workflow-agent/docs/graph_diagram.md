# Graph Diagram

```mermaid
flowchart TD
    A[receive_request] --> B[classify_request]
    B --> C[lookup_policy]
    C -->|success| D[draft_plan]
    C -->|retry| C
    C -->|recover| E[recover_policy]
    E --> D
    D -->|approval required| F[human_approval]
    D -->|no approval| G[execute_action]
    F -->|approved| G
    F -->|pending or rejected| H[finalize]
    G --> H
```

## Why This Graph Matters

The graph makes control flow visible:

- policy lookup failure loops are explicit;
- recovery is a named branch;
- human approval is a real gate before execution;
- final state inspection shows every node transition.
