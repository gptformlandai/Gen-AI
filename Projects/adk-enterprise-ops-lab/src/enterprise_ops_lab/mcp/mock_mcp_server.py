from __future__ import annotations

import argparse
import json


SERVICE_FIXTURES = {
    "payments-api": {
        "health": "degraded",
        "error_rate": 7.8,
        "deployments": ["checkout-fraud-enrichment-v42 deployed 18 minutes ago", "payments-api-v41 deployed yesterday"],
        "oncall": "payments-platform-oncall@example.com",
    },
    "search-service": {
        "health": "degraded",
        "error_rate": 5.4,
        "deployments": ["index-analyzer-v17 deployed 32 minutes ago"],
        "oncall": "search-platform-oncall@example.com",
    },
    "kafka-consumers": {
        "health": "warning",
        "error_rate": 1.6,
        "deployments": ["consumer-config-v9 deployed 2 hours ago"],
        "oncall": "data-platform-oncall@example.com",
    },
    "shared-postgres": {
        "health": "critical",
        "error_rate": 3.1,
        "deployments": ["reporting-job-v5 deployed 1 hour ago"],
        "oncall": "database-reliability-oncall@example.com",
    },
}


def handle_tool(tool_name: str, service: str) -> dict:
    fixture = SERVICE_FIXTURES.get(service, SERVICE_FIXTURES["payments-api"])
    if tool_name == "get_service_health":
        return {"service": service, "health": fixture["health"]}
    if tool_name == "get_recent_deployments":
        return {"service": service, "deployments": fixture["deployments"]}
    if tool_name == "get_error_rate":
        return {"service": service, "error_rate": fixture["error_rate"]}
    if tool_name == "get_oncall_owner":
        return {"service": service, "oncall_owner": fixture["oncall"]}
    raise ValueError(f"Unknown MCP tool: {tool_name}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Mock MCP operations server.")
    parser.add_argument("tool_name")
    parser.add_argument("--service", default="payments-api")
    args = parser.parse_args()
    print(json.dumps(handle_tool(args.tool_name, args.service), indent=2))


if __name__ == "__main__":
    main()

