from __future__ import annotations

import json

from structured_output_assistant.schemas import RequirementsDocument


SYSTEM_INSTRUCTIONS = """You are a senior product requirements analyst.
Your job is to convert messy stakeholder requests into implementation-ready structured requirements.
You do not chat casually. You return only a JSON object that matches the provided schema.
If the request is incomplete, return a needs_clarification document.
If the request asks for harmful or unauthorized behavior, return a refused document."""


DEVELOPER_INSTRUCTIONS = """Follow these developer constraints:
- Do not invent critical facts that the user did not provide.
- Prefer clear, testable requirements over vague feature descriptions.
- Include acceptance criteria when the status is ready.
- Use missing_information and clarification_questions when the request lacks enough detail.
- Use refusal_reason when the request is unsafe or unauthorized.
- Do not return Markdown fences, commentary, or extra fields."""


REPAIR_INSTRUCTIONS = """The previous response failed validation.
Return a corrected JSON object only.
Preserve the user's intent, remove extra fields, fix invalid types, and fill required fields only when they can be safely inferred.
If critical information cannot be inferred, return a needs_clarification document."""


def schema_as_json() -> str:
    """Expose the Pydantic schema as JSON for prompt-time schema grounding."""

    return json.dumps(RequirementsDocument.model_json_schema(), indent=2)


def build_generation_prompt(user_request: str) -> str:
    return f"""Convert this stakeholder request into the required JSON schema.

JSON schema:
{schema_as_json()}

Stakeholder request:
{user_request}
"""


def build_repair_prompt(
    user_request: str,
    previous_output: str,
    validation_errors: list[str],
) -> str:
    return f"""Repair the response so it validates against the schema.

JSON schema:
{schema_as_json()}

Original stakeholder request:
{user_request}

Previous response:
{previous_output}

Validation errors:
{json.dumps(validation_errors, indent=2)}
"""
