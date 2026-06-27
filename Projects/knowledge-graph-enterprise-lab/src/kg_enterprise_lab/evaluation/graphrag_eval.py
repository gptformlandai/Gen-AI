"""GraphRAG evaluation."""

from __future__ import annotations

from kg_enterprise_lab.graphrag.graphrag_pipeline import GraphRAGPipeline
from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository
from kg_enterprise_lab.schemas.evaluation import EvalCase, EvalResult
from kg_enterprise_lab.schemas.graphrag import GraphRAGRequest


def evaluate_graphrag(graph: InMemoryGraphRepository, cases: list[EvalCase]) -> list[EvalResult]:
    pipeline = GraphRAGPipeline(graph)
    results: list[EvalResult] = []
    for case in cases:
        response = pipeline.run(GraphRAGRequest(question=case.question or ""))
        text = f"{response.answer} {' '.join(chunk.text for chunk in response.evidence)}".lower()
        matched = [item for item in case.must_include if item.lower() in text]
        score = len(matched) / max(len(case.must_include), 1)
        results.append(EvalResult(case_id=case.id, passed=score == 1.0 and response.grounded, score=score, details=response.answer))
    return results
