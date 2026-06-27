"""Human-readable query explanations."""

from __future__ import annotations

from kg_enterprise_lab.schemas.query import QueryPlan


def explain_plan(plan: QueryPlan) -> list[str]:
    steps = [f"Classified intent as {plan.intent}."]
    if plan.entity_name:
        steps.append(f"Linked primary entity candidate: {plan.entity_name}.")
    if plan.target_name:
        steps.append(f"Linked target entity candidate: {plan.target_name}.")
    if plan.template_name:
        steps.append(f"Used allowlisted template: {plan.template_name}.")
    return steps
