from __future__ import annotations

import argparse
import json

from enterprise_ops_lab.tools.incident_tools import classify_intent, extract_incident_fields
from enterprise_ops_lab.tools.rag_tools import search_runbooks


EXPOSED_TOOLS = {
    "classify_intent": classify_intent,
    "extract_incident_fields": extract_incident_fields,
    "search_runbooks": search_runbooks,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Example MCP server exposing local ADK-style tools.")
    parser.add_argument("tool_name", choices=sorted(EXPOSED_TOOLS))
    parser.add_argument("--query", required=True)
    args = parser.parse_args()
    result = EXPOSED_TOOLS[args.tool_name](args.query)
    if hasattr(result, "model_dump"):
        result = result.model_dump(mode="json")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

