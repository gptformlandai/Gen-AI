from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


Status = Literal["ready", "needs_clarification", "refused"]
Confidence = Literal["high", "medium", "low"]
Priority = Literal["must", "should", "could"]


class RequirementItem(BaseModel):
    """One implementation-facing requirement with stable identity.

    The ID matters because real teams discuss, estimate, test, and change
    requirements over time. Stable IDs make those conversations traceable.
    """

    model_config = ConfigDict(extra="forbid")

    id: str = Field(description="Stable ID such as FR-001 or NFR-001.")
    priority: Priority = Field(description="Business priority.")
    description: str = Field(min_length=10)
    rationale: str = Field(default="", description="Why this requirement exists.")

    @field_validator("id")
    @classmethod
    def validate_requirement_id(cls, value: str) -> str:
        if not re.match(r"^(FR|NFR)-\d{3}$", value):
            raise ValueError("Requirement ID must look like FR-001 or NFR-001.")
        return value


class RequirementsDocument(BaseModel):
    """Validated contract returned by the assistant.

    This schema is the central Project 1 artifact. Everything else exists to
    protect this contract: prompts try to produce it, validation enforces it,
    repair attempts to recover it, and tests guard it.
    """

    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=5)
    status: Status
    problem_statement: str = Field(min_length=10)
    target_users: list[str] = Field(default_factory=list)
    functional_requirements: list[RequirementItem] = Field(default_factory=list)
    non_functional_requirements: list[RequirementItem] = Field(default_factory=list)
    acceptance_criteria: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    clarification_questions: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    confidence: Confidence
    refusal_reason: str = Field(default="")

    @model_validator(mode="after")
    def validate_status_contract(self) -> "RequirementsDocument":
        """Enforce business rules that plain JSON Schema cannot express well."""

        if self.status == "ready":
            if not self.target_users:
                raise ValueError("Ready documents must include at least one target user.")
            if not self.functional_requirements:
                raise ValueError("Ready documents must include functional requirements.")
            if not self.acceptance_criteria:
                raise ValueError("Ready documents must include acceptance criteria.")
            if self.refusal_reason:
                raise ValueError("Ready documents cannot include a refusal reason.")

        if self.status == "needs_clarification":
            if not self.missing_information:
                raise ValueError("Clarification documents must list missing information.")
            if not self.clarification_questions:
                raise ValueError("Clarification documents must ask clarification questions.")
            if self.confidence == "high":
                raise ValueError("Clarification documents cannot have high confidence.")

        if self.status == "refused":
            if not self.refusal_reason:
                raise ValueError("Refused documents must include a refusal reason.")
            if self.confidence != "low":
                raise ValueError("Refused documents should use low confidence.")

        return self


class AssistantRunResult(BaseModel):
    """Stable envelope returned by the graph and CLI."""

    model_config = ConfigDict(extra="forbid")

    request: str
    status: Literal["ready", "needs_clarification", "refused", "schema_error"]
    attempts: int
    output: RequirementsDocument | None = None
    errors: list[str] = Field(default_factory=list)


def build_clarification_document(raw_request: str, reason: str) -> RequirementsDocument:
    """Create a valid response when the input lacks critical context."""

    return RequirementsDocument(
        title="Clarification Needed",
        status="needs_clarification",
        problem_statement=f"The request is not specific enough to produce implementation-ready requirements: {reason}",
        target_users=[],
        missing_information=[
            "Target user or persona",
            "Concrete workflow or feature goal",
            "Success criteria or expected outcome",
        ],
        clarification_questions=[
            "Who is the primary user for this feature?",
            "What workflow should the system support first?",
            "What outcome would make this feature successful?",
        ],
        assumptions=[],
        confidence="low",
    )


def build_refusal_document(raw_request: str, reason: str) -> RequirementsDocument:
    """Create a valid refusal while preserving the structured contract."""

    return RequirementsDocument(
        title="Request Refused",
        status="refused",
        problem_statement="The request asks for behavior that should not be turned into implementation requirements.",
        target_users=[],
        risks=["The requested behavior could enable harm, unauthorized access, or policy violations."],
        missing_information=[],
        clarification_questions=[],
        assumptions=[],
        confidence="low",
        refusal_reason=reason,
    )
