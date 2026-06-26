from enterprise_ops_lab.tools.mcp_client_tools import get_error_rate, get_service_health


def test_mcp_health_and_error_rate_are_normalized() -> None:
    health = get_service_health("payments-api")
    errors = get_error_rate("payments-api")

    assert health["ok"] is True
    assert health["data"]["health"] == "degraded"
    assert errors["data"]["error_rate"] > 0

