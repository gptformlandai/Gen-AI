from __future__ import annotations

from enterprise_ops_lab.schemas.incident import EvidenceItem


def generate_grounded_answer(question: str, evidence: list[EvidenceItem]) -> str:
    if not evidence:
        return "No sufficiently relevant runbook evidence was found."
    bullets = []
    for item in evidence[:3]:
        excerpt = item.quote[:240].strip()
        bullets.append(f"- {excerpt} [source: {item.source}]")
    return f"Grounded answer for: {question}\n" + "\n".join(bullets)

