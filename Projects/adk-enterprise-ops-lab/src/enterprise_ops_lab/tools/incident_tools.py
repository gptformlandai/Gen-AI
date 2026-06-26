from __future__ import annotations

from enterprise_ops_lab.schemas.incident import IncidentTriage


def classify_intent(query: str) -> str:
    lower = query.lower()
    if "remember" in lower:
        return "remember_resolution"
    if "evaluate" in lower:
        return "evaluate_trajectory"
    if "show me how" in lower or "tool" in lower and "used" in lower:
        return "show_tool_trace"
    if "report" in lower or "artifact" in lower:
        return "generate_report"
    if "session state" in lower or "memory" in lower:
        return "demonstrate_state_memory"
    if "runbook" in lower or "search" in lower:
        return "search_runbook"
    return "investigate_incident"


def extract_incident_fields(query: str) -> IncidentTriage:
    lower = query.lower()
    service = infer_service(lower)
    severity = infer_severity(lower, service)
    symptoms = infer_symptoms(lower)
    domain = infer_domain(service, lower)
    confidence = 0.88 if service != "unknown-service" and symptoms else 0.55
    questions = []
    if service == "unknown-service":
        questions.append("Which service is affected?")
    if not symptoms:
        questions.append("What symptoms or metrics are visible?")
    return IncidentTriage(
        intent=classify_intent(query),
        service=service,
        severity=severity,
        symptoms=symptoms,
        suspected_domain=domain,
        confidence=confidence,
        needs_clarification=bool(questions),
        clarification_questions=questions,
    )


def infer_service(lower: str) -> str:
    if "payment" in lower or "checkout" in lower:
        return "payments-api"
    if "kafka" in lower or "consumer lag" in lower:
        return "kafka-consumers"
    if "search-service" in lower or "search service" in lower or "search errors" in lower:
        return "search-service"
    if "database" in lower or "postgres" in lower or "db " in lower:
        return "shared-postgres"
    return "unknown-service"


def infer_severity(lower: str, service: str) -> str:
    if any(term in lower for term in ("down", "cannot", "checkout", "critical", "sev1")) or service in {"payments-api", "shared-postgres"}:
        return "sev1"
    if any(term in lower for term in ("latency", "lag", "errors", "degraded", "sev2")):
        return "sev2"
    return "sev3"


def infer_symptoms(lower: str) -> list[str]:
    symptoms = []
    for term in ["latency", "errors", "lag", "deployment", "database", "health", "timeout"]:
        if term in lower:
            symptoms.append(term)
    return symptoms


def infer_domain(service: str, lower: str) -> str:
    if service == "payments-api":
        return "payments"
    if service == "search-service":
        return "search"
    if service == "kafka-consumers":
        return "streaming"
    if service == "shared-postgres":
        return "database"
    return "operations"
