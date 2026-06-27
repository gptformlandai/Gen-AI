"""Safe query executor over allowlisted handlers."""

from __future__ import annotations

from kg_enterprise_lab.query.graph_query_service import GraphQueryService
from kg_enterprise_lab.schemas.query import QueryPlan, QueryRequest, QueryResponse


class SafeQueryExecutor:
    def __init__(self, service: GraphQueryService) -> None:
        self.service = service
        self.allowed_intents = {
            "dependents",
            "blast_radius",
            "shortest_path",
            "ownership",
            "similar_incidents",
            "runbook_search",
            "lineage",
            "centrality",
            "validate",
            "duplicates",
            "rdf_compare",
            "generic",
        }

    def execute(self, request: QueryRequest, plan: QueryPlan) -> QueryResponse:
        if plan.intent not in self.allowed_intents:
            raise ValueError(f"Intent is not allowlisted: {plan.intent}")
        return self.service.answer(request, plan)
