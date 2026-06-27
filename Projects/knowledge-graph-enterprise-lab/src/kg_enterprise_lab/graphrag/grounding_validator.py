"""Grounding checks for generated GraphRAG answers."""

from __future__ import annotations

from kg_enterprise_lab.schemas.graphrag import EvidenceChunk


def validate_grounding(answer: str, evidence: list[EvidenceChunk]) -> tuple[bool, list[str]]:
    evidence_text = " ".join(chunk.text for chunk in evidence).lower()
    notes: list[str] = []
    for important in ["incident", "service", "runbook"]:
        if important in answer.lower() and important not in evidence_text:
            notes.append(f"Answer mentions {important} but evidence does not.")
    return (len(notes) == 0, notes)
