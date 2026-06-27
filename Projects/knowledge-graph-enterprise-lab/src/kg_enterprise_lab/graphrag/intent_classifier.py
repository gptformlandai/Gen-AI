"""GraphRAG intent classifier."""

from __future__ import annotations

from kg_enterprise_lab.query.query_intent_classifier import classify_intent


def classify_graphrag_intent(question: str) -> str:
    base_intent = classify_intent(question)
    if base_intent == "generic" and any(term in question.lower() for term in ["why", "explain", "slow", "latency"]):
        return "root_cause_explanation"
    return base_intent
