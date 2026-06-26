from __future__ import annotations

import json

from enterprise_ops_lab.agents.mcp_operations_agent import run


if __name__ == "__main__":
    print(json.dumps(run("payments-api").model_dump(mode="json"), indent=2))

