"""Plan graph queries from natural language."""

from __future__ import annotations

import re

from kg_enterprise_lab.query.query_intent_classifier import classify_intent
from kg_enterprise_lab.schemas.query import QueryPlan, QueryRequest


def plan_query(request: QueryRequest) -> QueryPlan:
    question = request.question.strip()
    intent = classify_intent(question)
    entity_name = _extract_entity(question)
    target_name = _extract_target(question)
    template_name = intent if intent in {"dependents", "blast_radius", "lineage", "ownership"} else None
    return QueryPlan(intent=intent, entity_name=entity_name, target_name=target_name, template_name=template_name, max_depth=request.max_depth)


def _extract_entity(question: str) -> str | None:
    patterns = [
        r"between ([A-Za-z0-9_-]+) and",
        r"depend on ([A-Za-z0-9_-]+)",
        r"depends on ([A-Za-z0-9_-]+)",
        r"for ([A-Za-z0-9_-]+)",
        r"of ([A-Za-z0-9_-]+)",
        r"from ([A-Za-z0-9_-]+)",
        r"why ([A-Za-z0-9_-]+)",
        r"by ([A-Z]+-\d+)",
        r"by ([A-Za-z0-9_-]+)",
        r"(INC-\d+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, question, flags=re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def _extract_target(question: str) -> str | None:
    match = re.search(r"between ([A-Za-z0-9_-]+) and ([A-Za-z0-9_-]+)", question, flags=re.IGNORECASE)
    if match:
        return match.group(2)
    return None
