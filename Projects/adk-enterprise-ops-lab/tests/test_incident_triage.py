from enterprise_ops_lab.tools.incident_tools import extract_incident_fields


def test_triage_extracts_service_and_severity() -> None:
    triage = extract_incident_fields("Investigate high latency in payments-api after last deployment.")

    assert triage.service == "payments-api"
    assert triage.severity == "sev1"
    assert "latency" in triage.symptoms

