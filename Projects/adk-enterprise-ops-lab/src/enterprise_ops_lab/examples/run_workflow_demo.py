from __future__ import annotations

import json

from enterprise_ops_lab.agents.mcp_operations_agent import run as run_mcp
from enterprise_ops_lab.agents.investigation_workflow_agent import run as run_workflow


if __name__ == "__main__":
    mcp = run_mcp("shared-postgres")
    timeline = run_workflow("shared-postgres", ["database", "latency"], mcp)
    print(json.dumps([item.model_dump(mode="json") for item in timeline], indent=2))

