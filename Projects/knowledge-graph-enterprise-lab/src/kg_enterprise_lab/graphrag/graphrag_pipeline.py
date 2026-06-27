"""End-to-end GraphRAG pipeline."""

from __future__ import annotations

from kg_enterprise_lab.embeddings.vector_index import LocalVectorIndex
from kg_enterprise_lab.graphrag.answer_generator import MockAnswerGenerator
from kg_enterprise_lab.graphrag.entity_linker import EntityLinker
from kg_enterprise_lab.graphrag.graph_retriever import GraphRetriever
from kg_enterprise_lab.graphrag.grounding_validator import validate_grounding
from kg_enterprise_lab.graphrag.hybrid_retriever import HybridRetriever
from kg_enterprise_lab.graphrag.intent_classifier import classify_graphrag_intent
from kg_enterprise_lab.graphrag.vector_retriever import VectorRetriever
from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository
from kg_enterprise_lab.observability.metrics import Metrics
from kg_enterprise_lab.schemas.graphrag import GraphRAGRequest, GraphRAGResponse, GraphRAGTrace


class GraphRAGPipeline:
    def __init__(self, graph: InMemoryGraphRepository) -> None:
        self.graph = graph
        self.vector_index = LocalVectorIndex()
        self.vector_index.index_graph(graph)
        self.linker = EntityLinker(graph)
        self.graph_retriever = GraphRetriever(graph)
        self.vector_retriever = VectorRetriever(self.vector_index)
        self.hybrid_retriever = HybridRetriever(graph, self.vector_index)
        self.generator = MockAnswerGenerator()
        self.metrics = Metrics()

    def run(self, request: GraphRAGRequest) -> GraphRAGResponse:
        self.metrics.increment("graphrag.requests")
        intent = classify_graphrag_intent(request.question)
        linked = self.linker.link(request.question)
        graph_evidence, node_ids, rel_ids = self.graph_retriever.retrieve(linked, request.max_graph_depth)
        vector_evidence = self.vector_retriever.retrieve(request.question, request.vector_top_k)
        hybrid_evidence = self.hybrid_retriever.retrieve(request.question, linked, top_k=request.vector_top_k)
        evidence = _dedupe_evidence(graph_evidence + hybrid_evidence + vector_evidence)
        returned_evidence = _ensure_channel_coverage(evidence, hybrid_evidence, max_items=12)
        answer = self.generator.generate(request.question, self.graph, evidence)
        grounded, notes = validate_grounding(answer, evidence)
        confidence = 0.9 if grounded and linked else 0.65 if grounded else 0.45
        self.metrics.increment("graphrag.grounded" if grounded else "graphrag.ungrounded")
        trace = GraphRAGTrace(
            intent=intent,
            linked_entities=linked,
            graph_steps=[f"Retrieved {len(node_ids)} nodes and {len(rel_ids)} relationships."],
            vector_steps=[f"Retrieved {len(vector_evidence)} vector hits."],
            hybrid_steps=[f"Retrieved {len(hybrid_evidence)} hybrid graph+vector hits.", f"Metrics: {self.metrics.snapshot()['counters']}"],
            guardrail_notes=notes,
        )
        return GraphRAGResponse(question=request.question, answer=answer, evidence=returned_evidence, trace=trace, confidence=confidence, grounded=grounded)


def _dedupe_evidence(evidence: list) -> list:
    seen: set[str] = set()
    deduped = []
    for chunk in sorted(evidence, key=lambda item: item.score, reverse=True):
        key = chunk.id
        if key not in seen:
            seen.add(key)
            deduped.append(chunk)
    return deduped


def _ensure_channel_coverage(evidence: list, hybrid_evidence: list, max_items: int) -> list:
    selected = evidence[:max_items]
    if hybrid_evidence and not any(chunk.source == "hybrid" for chunk in selected):
        selected = selected[: max_items - 1] + [hybrid_evidence[0]]
    return selected
