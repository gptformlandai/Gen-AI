from kg_enterprise_lab.governance.query_policy import is_allowed_intent
from kg_enterprise_lab.governance.redaction import redact_sensitive_text
from kg_enterprise_lab.governance.risk_checker import check_traversal_depth


def test_governance_controls():
    assert is_allowed_intent("blast_radius")
    assert check_traversal_depth(10)
    assert "arya.patel@example.com" not in redact_sensitive_text("Contact arya.patel@example.com")
