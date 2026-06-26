from __future__ import annotations

import pytest
from pydantic import ValidationError

from structured_output_assistant.llm import RuleBasedRequirementsModel
from structured_output_assistant.schemas import RequirementsDocument
from structured_output_assistant.validation import parse_requirements_document


def test_ready_document_requires_acceptance_criteria() -> None:
    payload = {
        "title": "Vendor Workflow",
        "status": "ready",
        "problem_statement": "Employees need a workflow to onboard vendors.",
        "target_users": ["employees"],
        "functional_requirements": [
            {
                "id": "FR-001",
                "priority": "must",
                "description": "The system shall allow employees to submit vendor details.",
                "rationale": "Needed to start the workflow.",
            }
        ],
        "non_functional_requirements": [],
        "acceptance_criteria": [],
        "constraints": [],
        "dependencies": [],
        "risks": [],
        "missing_information": [],
        "clarification_questions": [],
        "assumptions": [],
        "confidence": "medium",
        "refusal_reason": "",
    }

    with pytest.raises(ValidationError):
        RequirementsDocument.model_validate(payload)


def test_extra_fields_are_rejected() -> None:
    model = RuleBasedRequirementsModel()
    payload = parse_requirements_document(
        model.generate(
            "Build a dashboard for support leads to view ticket volume and export reports."
        )
    ).model_dump()
    payload["unexpected_field"] = "should fail"

    with pytest.raises(ValidationError):
        RequirementsDocument.model_validate(payload)


def test_markdown_wrapped_json_can_be_parsed() -> None:
    model = RuleBasedRequirementsModel()
    raw_json = model.generate(
        "Create role-based access for admins and reviewers with audit logs."
    )
    parsed = parse_requirements_document(f"```json\n{raw_json}\n```")

    assert parsed.status == "ready"
    assert parsed.functional_requirements


def test_rule_based_repair_recovers_from_unparseable_output() -> None:
    model = RuleBasedRequirementsModel()
    repaired = model.repair(
        user_request="Build onboarding reminders for HR and managers.",
        previous_output="not json at all",
        validation_errors=["No JSON object found in model output."],
    )
    parsed = parse_requirements_document(repaired)

    assert parsed.status == "ready"
    assert parsed.acceptance_criteria
