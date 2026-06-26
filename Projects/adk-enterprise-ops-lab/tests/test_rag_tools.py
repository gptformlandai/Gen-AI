from enterprise_ops_lab.tools.rag_tools import search_runbooks


def test_rag_search_returns_payments_source() -> None:
    result = search_runbooks("payments-api high latency after deployment", service="payments-api")

    assert result["evidence"]
    assert "payments_api_runbook.md" in result["sources"]

