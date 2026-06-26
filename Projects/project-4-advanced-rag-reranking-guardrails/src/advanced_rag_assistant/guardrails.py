from __future__ import annotations

from advanced_rag_assistant.schemas import GuardrailDecision


UNSAFE_PATTERNS = (
    "bypass login",
    "bypass authentication",
    "steal password",
    "steal credentials",
    "disable audit",
    "hide user actions",
)

AUDIT_ROLES = {"auditor", "admin", "security", "compliance"}
ROLE_ADMIN_ROLES = {"admin", "security"}


class GuardrailEngine:
    """Safety and permission checks that run before retrieval."""

    def check(self, question: str, user_role: str) -> GuardrailDecision:
        lower = question.lower()
        normalized_role = user_role.lower()

        if any(pattern in lower for pattern in UNSAFE_PATTERNS):
            return GuardrailDecision(
                allowed=False,
                reason="The question asks for unsafe credential or control-bypass behavior.",
                policy="safety_refusal",
            )

        if ("audit trail" in lower or "user actions" in lower) and normalized_role not in AUDIT_ROLES:
            return GuardrailDecision(
                allowed=False,
                reason="Audit-trail details require auditor, admin, security, or compliance role.",
                policy="permission_refusal",
            )

        if ("admin" in lower and "role" in lower or "user roles" in lower) and normalized_role not in ROLE_ADMIN_ROLES:
            return GuardrailDecision(
                allowed=False,
                reason="Role-management details require admin or security role.",
                policy="permission_refusal",
            )

        return GuardrailDecision(allowed=True, reason="Allowed", policy="allowed")
