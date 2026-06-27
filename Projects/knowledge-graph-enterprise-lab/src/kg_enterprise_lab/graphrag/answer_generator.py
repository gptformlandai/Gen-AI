"""Mock answer generator that behaves like a constrained LLM adapter."""

from __future__ import annotations

from kg_enterprise_lab.graph.in_memory_graph import InMemoryGraphRepository
from kg_enterprise_lab.schemas.graphrag import EvidenceChunk


class MockAnswerGenerator:
    def generate(self, question: str, graph: InMemoryGraphRepository, evidence: list[EvidenceChunk]) -> str:
        lowered = question.lower()
        if "provider-search-service" in lowered and ("slow" in lowered or "latency" in lowered):
            incident = graph.get_node("INC-1001")
            service = graph.get_node("svc-provider-search")
            provider_db = graph.get_node("svc-provider-db")
            runbook = graph.get_node("runbook-provider-latency")
            return (
                f"{service.name if service else 'provider-search-service'} may be slow because {incident.id if incident else 'INC-1001'} "
                f"links Provider Search latency to provider directory import lag and database timeout symptoms. "
                f"The graph connects the service to {provider_db.name if provider_db else 'provider-db'} and to "
                f"{runbook.id if runbook else 'runbook-provider-latency'}, so the first checks are DB locks, topic lag, and cache warmup."
            )
        top_nodes = []
        for chunk in evidence[:5]:
            top_nodes.extend(chunk.node_ids)
        unique = []
        for node_id in top_nodes:
            if node_id not in unique and graph.get_node(node_id):
                unique.append(node_id)
        names = ", ".join(graph.get_node(node_id).name for node_id in unique)
        return f"GraphRAG retrieved graph and vector evidence around: {names}. Use the cited nodes and relationships to inspect dependencies, owners, incidents, and runbooks."
