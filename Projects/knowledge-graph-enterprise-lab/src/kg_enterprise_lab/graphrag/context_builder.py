"""Build concise grounded context from graph and vector evidence."""

from __future__ import annotations

from kg_enterprise_lab.schemas.graphrag import EvidenceChunk


def build_context(evidence: list[EvidenceChunk], limit: int = 12) -> str:
    ranked = sorted(evidence, key=lambda chunk: chunk.score, reverse=True)[:limit]
    return "\n".join(f"[{chunk.id}] {chunk.text}" for chunk in ranked)
