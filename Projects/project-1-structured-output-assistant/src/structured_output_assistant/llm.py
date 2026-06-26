from __future__ import annotations

import json
import re
from typing import Protocol

from structured_output_assistant.prompts import (
    DEVELOPER_INSTRUCTIONS,
    REPAIR_INSTRUCTIONS,
    SYSTEM_INSTRUCTIONS,
    build_generation_prompt,
    build_repair_prompt,
    schema_as_json,
)
from structured_output_assistant.schemas import (
    RequirementsDocument,
    build_clarification_document,
    build_refusal_document,
)
from structured_output_assistant.validation import OutputParseError, parse_json_dict


class RequirementsModel(Protocol):
    """Small interface that lets the graph use local or real LLM backends."""

    def generate(self, user_request: str) -> str:
        ...

    def repair(
        self,
        user_request: str,
        previous_output: str,
        validation_errors: list[str],
    ) -> str:
        ...


RISKY_TERMS = (
    "steal passwords",
    "steals passwords",
    "stealing passwords",
    "bypass authentication",
    "bypasses authentication",
    "bypassing authentication",
    "disable audit",
    "hide from audit",
    "malware",
    "phishing",
    "exfiltrate",
    "credential theft",
)


VAGUE_PATTERNS = (
    "make the app better",
    "something with ai",
    "improve the system",
    "make it modern",
)


FEATURE_KEYWORDS = (
    "approve",
    "dashboard",
    "export",
    "notify",
    "upload",
    "search",
    "filter",
    "report",
    "reminder",
    "onboarding",
    "access",
    "role",
    "workflow",
    "audit",
    "csv",
    "ticket",
)


def contains_risky_request(user_request: str) -> bool:
    lower = user_request.lower()
    return any(term in lower for term in RISKY_TERMS)


def looks_incomplete(user_request: str) -> bool:
    """Cheap precheck before spending an LLM call.

    This is not meant to understand the whole request. It catches obviously
    underspecified inputs so the assistant asks questions instead of guessing.
    """

    lower = user_request.lower().strip()
    if len(lower) < 35:
        return True
    if any(pattern in lower for pattern in VAGUE_PATTERNS):
        return True
    return not any(keyword in lower for keyword in FEATURE_KEYWORDS)


class RuleBasedRequirementsModel:
    """Deterministic model used by tests and offline demos.

    It is intentionally simple. Its job is to prove the control flow and schema
    discipline without requiring a live model key. The OpenAI-backed LangChain
    adapter below can be used once we want realistic model behavior.
    """

    def generate(self, user_request: str) -> str:
        if contains_risky_request(user_request):
            return build_refusal_document(
                user_request,
                "The request appears to involve credential theft, evasion, or unauthorized access.",
            ).model_dump_json(indent=2)

        if looks_incomplete(user_request):
            return build_clarification_document(
                user_request,
                "The request does not identify enough concrete workflow, user, or outcome detail.",
            ).model_dump_json(indent=2)

        return self._build_ready_document(user_request).model_dump_json(indent=2)

    def repair(
        self,
        user_request: str,
        previous_output: str,
        validation_errors: list[str],
    ) -> str:
        try:
            payload = parse_json_dict(previous_output)
        except OutputParseError:
            return self.generate(user_request)

        # Repair strategy for the deterministic path: keep what can be trusted,
        # then rebuild missing contract fields with conservative defaults.
        repaired = self._build_ready_document(user_request).model_dump()
        repaired.update({key: value for key, value in payload.items() if key in repaired})

        if repaired.get("status") == "needs_clarification":
            return build_clarification_document(
                user_request,
                "The previous model output marked the request incomplete.",
            ).model_dump_json(indent=2)
        if repaired.get("status") == "refused":
            return build_refusal_document(
                user_request,
                repaired.get("refusal_reason") or "The request cannot be safely fulfilled.",
            ).model_dump_json(indent=2)

        return json.dumps(repaired, indent=2)

    def _build_ready_document(self, user_request: str) -> RequirementsDocument:
        sentences = self._sentences(user_request)
        target_users = self._target_users(user_request)
        title = self._title_from_request(sentences[0])
        main_noun = self._main_feature_hint(user_request)

        functional_requirements = []
        for index, sentence in enumerate(sentences[:4], start=1):
            functional_requirements.append(
                {
                    "id": f"FR-{index:03d}",
                    "priority": "must" if index <= 2 else "should",
                    "description": self._requirement_sentence(sentence),
                    "rationale": "Captured from the stakeholder request.",
                }
            )

        if not functional_requirements:
            functional_requirements.append(
                {
                    "id": "FR-001",
                    "priority": "must",
                    "description": f"The system shall support the requested {main_noun} workflow.",
                    "rationale": "Minimum functional requirement inferred from the request.",
                }
            )

        non_functional_requirements = [
            {
                "id": "NFR-001",
                "priority": "should",
                "description": "The system should record important user actions for troubleshooting and auditability.",
                "rationale": "Structured requirements should capture reliability and traceability expectations.",
            }
        ]

        if any(term in user_request.lower() for term in ("secure", "access", "role", "audit")):
            non_functional_requirements.append(
                {
                    "id": "NFR-002",
                    "priority": "must",
                    "description": "The system must enforce authorization checks before sensitive actions are completed.",
                    "rationale": "The request mentions access, roles, security, or audit behavior.",
                }
            )

        return RequirementsDocument(
            title=title,
            status="ready",
            problem_statement=f"Stakeholders need a reliable way to support this workflow: {self._shorten(user_request, 220)}",
            target_users=target_users,
            functional_requirements=functional_requirements,
            non_functional_requirements=non_functional_requirements,
            acceptance_criteria=[
                f"Given a valid {main_noun} request, when the user completes the primary workflow, then the system records the outcome.",
                "Given missing or invalid input, when the user submits the workflow, then the system returns a clear validation message.",
                "Given an authorized user, when they view the feature, then they see the current status and relevant history.",
            ],
            constraints=[],
            dependencies=[],
            risks=[
                "The request may still need product-owner review before implementation.",
                "Some edge cases may be missing from the initial stakeholder description.",
            ],
            missing_information=[],
            clarification_questions=[],
            assumptions=[
                "Authentication and basic user identity already exist.",
                "The first version should prioritize the core workflow before advanced analytics.",
            ],
            confidence="medium",
        )

    def _sentences(self, text: str) -> list[str]:
        candidates = re.split(r"[.\n;]+", text)
        return [candidate.strip() for candidate in candidates if len(candidate.strip()) >= 10]

    def _title_from_request(self, first_sentence: str) -> str:
        cleaned = re.sub(r"^(we need|build|create|for)\s+", "", first_sentence.strip(), flags=re.I)
        return self._shorten(cleaned[:1].upper() + cleaned[1:], 80)

    def _target_users(self, text: str) -> list[str]:
        lower = text.lower()
        users = []
        for label in ("employees", "managers", "admins", "reviewers", "customers", "analysts", "support leads", "hr", "finance"):
            if label in lower:
                users.append(label)
        return users or ["end users"]

    def _requirement_sentence(self, sentence: str) -> str:
        cleaned = sentence.strip()
        if cleaned.lower().startswith(("the system", "users", "admins", "managers", "customers")):
            return cleaned
        return f"The system shall support this behavior: {cleaned}"

    def _main_feature_hint(self, text: str) -> str:
        lower = text.lower()
        for keyword in FEATURE_KEYWORDS:
            if keyword in lower:
                return keyword
        return "feature"

    def _shorten(self, text: str, limit: int) -> str:
        stripped = " ".join(text.split())
        return stripped if len(stripped) <= limit else stripped[: limit - 3].rstrip() + "..."


class LangChainRequirementsModel:
    """LangChain adapter for live model calls.

    LangGraph owns the workflow. LangChain is used only as integration glue for
    the chat model call, which keeps orchestration and provider access separate.
    """

    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.0) -> None:
        self.model = model
        self.temperature = temperature
        self._chat = None

    def generate(self, user_request: str) -> str:
        return self._invoke(
            system_text=f"{SYSTEM_INSTRUCTIONS}\n\nDeveloper instructions:\n{DEVELOPER_INSTRUCTIONS}",
            user_text=build_generation_prompt(user_request),
        )

    def repair(
        self,
        user_request: str,
        previous_output: str,
        validation_errors: list[str],
    ) -> str:
        return self._invoke(
            system_text=f"{SYSTEM_INSTRUCTIONS}\n\n{REPAIR_INSTRUCTIONS}",
            user_text=build_repair_prompt(user_request, previous_output, validation_errors),
        )

    def _invoke(self, system_text: str, user_text: str) -> str:
        try:
            from langchain_core.messages import HumanMessage, SystemMessage
            from langchain_openai import ChatOpenAI
        except ImportError as error:
            raise RuntimeError(
                "LangChain OpenAI dependencies are missing. Install this project with python -m pip install -e ."
            ) from error

        if self._chat is None:
            self._chat = ChatOpenAI(model=self.model, temperature=self.temperature)

        response = self._chat.invoke(
            [
                SystemMessage(content=system_text),
                HumanMessage(content=f"{user_text}\n\nSchema cache:\n{schema_as_json()}"),
            ]
        )
        return str(response.content)
