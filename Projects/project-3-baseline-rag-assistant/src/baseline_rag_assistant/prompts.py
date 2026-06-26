from __future__ import annotations

from baseline_rag_assistant.schemas import Citation


SYSTEM_PROMPT = """You are a grounded support knowledge-base assistant.
Answer only from the evidence packet.
Every factual claim must be supported by a citation ID.
If the evidence packet does not contain enough information, refuse briefly."""


ANSWER_CONTRACT = """Return:
1. A concise answer in plain English.
2. Inline citation IDs such as [S1].
3. No outside knowledge.
4. A refusal if the evidence is weak or unrelated."""


def build_evidence_packet(question: str, citations: list[Citation]) -> str:
    """Separate retrieved evidence from final answer instructions."""

    lines = [f"Question: {question}", "", "Evidence packet:"]
    for citation in citations:
        lines.append(f"[{citation.citation_id}] {citation.title}")
        lines.append(f"Quote: {citation.quote}")
        lines.append(f"Metadata: {citation.metadata}")
        lines.append("")
    lines.append("Answer contract:")
    lines.append(ANSWER_CONTRACT)
    return "\n".join(lines)
