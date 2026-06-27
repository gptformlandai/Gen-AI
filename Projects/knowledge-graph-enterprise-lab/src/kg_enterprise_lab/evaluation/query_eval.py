"""Graph query evaluation."""

from __future__ import annotations

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository
from kg_enterprise_lab.query.graph_query_service import GraphQueryService
from kg_enterprise_lab.schemas.evaluation import EvalCase, EvalResult
from kg_enterprise_lab.schemas.query import QueryRequest


def evaluate_queries(graph: InMemoryGraphRepository, cases: list[EvalCase]) -> list[EvalResult]:
    service = GraphQueryService(graph)
    results: list[EvalResult] = []
    for case in cases:
        response = service.answer(QueryRequest(question=case.question or ""))
        answer_text = f"{response.answer} {' '.join(response.node_ids)}".lower()
        matched = [item for item in case.must_include if item.lower() in answer_text]
        score = len(matched) / max(len(case.must_include), 1)
        results.append(EvalResult(case_id=case.id, passed=score == 1.0, score=score, details=response.answer))
    return results
