from __future__ import annotations

from enterprise_ops_lab.mcp.mcp_client import MockMcpClient


def get_service_health(service: str) -> dict:
    return MockMcpClient().get_service_health(service).model_dump(mode="json")


def get_recent_deployments(service: str) -> dict:
    return MockMcpClient().get_recent_deployments(service).model_dump(mode="json")


def get_error_rate(service: str) -> dict:
    return MockMcpClient().get_error_rate(service).model_dump(mode="json")


def get_oncall_owner(service: str) -> dict:
    return MockMcpClient().get_oncall_owner(service).model_dump(mode="json")

