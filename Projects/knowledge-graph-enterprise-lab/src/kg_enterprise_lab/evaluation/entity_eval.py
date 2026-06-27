"""Entity extraction evaluation."""

from __future__ import annotations

from kg_enterprise_lab.extraction.entity_extractor import EntityExtractor
from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository
from kg_enterprise_lab.schemas.evaluation import EvalCase, EvalResult
from kg_enterprise_lab.schemas.extraction import SourceDocument


def evaluate_entity_extraction(graph: InMemoryGraphRepository, cases: list[EvalCase]) -> list[EvalResult]:
    extractor = EntityExtractor(graph)
    results: list[EvalResult] = []
    for case in cases:
        document = SourceDocument(id=case.id, source_type="eval", text=case.text or "")
        found = {entity.name for entity in extractor.extract(document)} | {entity.canonical_id for entity in extractor.extract(document)}
        expected = set(case.expected_entities)
        matched = {item for item in expected if item in found}
        score = len(matched) / max(len(expected), 1)
        results.append(EvalResult(case_id=case.id, passed=score == 1.0, score=score, details=f"matched={sorted(matched)} expected={sorted(expected)}"))
    return results
