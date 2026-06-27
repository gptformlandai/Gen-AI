"""Relationship extraction evaluation."""

from __future__ import annotations

from kg_enterprise_lab.extraction.relationship_extractor import RelationshipExtractor
from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository
from kg_enterprise_lab.schemas.evaluation import EvalCase, EvalResult
from kg_enterprise_lab.schemas.extraction import SourceDocument


def evaluate_relationship_extraction(graph: InMemoryGraphRepository, cases: list[EvalCase]) -> list[EvalResult]:
    extractor = RelationshipExtractor(graph)
    results: list[EvalResult] = []
    for case in cases:
        document = SourceDocument(id=case.id, source_type="eval", text=case.text or "")
        found = {(rel.source_name, rel.relationship_type, rel.target_name) for rel in extractor.extract(document)}
        expected = {tuple(item) for item in case.expected_relationships}
        matched = expected & found
        score = len(matched) / max(len(expected), 1)
        results.append(EvalResult(case_id=case.id, passed=score == 1.0, score=score, details=f"matched={sorted(matched)} expected={sorted(expected)}"))
    return results
