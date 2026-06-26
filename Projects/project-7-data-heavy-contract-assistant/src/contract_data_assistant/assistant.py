from __future__ import annotations

from contract_data_assistant.index import StructuredContractIndex
from contract_data_assistant.schemas import AssistantAnswer, Citation, SearchHit


class ContractDataAssistant:
    """Answers from typed contract elements with citations."""

    def __init__(self, index: StructuredContractIndex) -> None:
        self.index = index

    def answer(self, question: str, k: int = 4) -> AssistantAnswer:
        hits = self.index.search(question, k=k)
        if not hits:
            return AssistantAnswer(
                question=question,
                answer="I could not find enough structured contract evidence to answer.",
                citations=[],
                confidence="low",
            )

        citations = [build_citation(hit, index + 1) for index, hit in enumerate(dedupe_hits(hits))]
        answer = synthesize_answer(question, citations)
        confidence = "high" if hits[0].score >= 7 else "medium"
        return AssistantAnswer(question=question, answer=answer, citations=citations, confidence=confidence)


def dedupe_hits(hits: list[SearchHit]) -> list[SearchHit]:
    seen_text: set[str] = set()
    deduped: list[SearchHit] = []
    for hit in hits:
        if hit.element.text in seen_text:
            continue
        seen_text.add(hit.element.text)
        deduped.append(hit)
        if len(deduped) == 3:
            break
    return deduped


def build_citation(hit: SearchHit, citation_number: int) -> Citation:
    return Citation(
        citation_id=f"S{citation_number}",
        document_id=hit.element.document_id,
        element_id=hit.element.id,
        kind=hit.element.kind,
        title=hit.element.title,
        quote=hit.element.text,
        metadata=hit.element.metadata,
    )


def synthesize_answer(question: str, citations: list[Citation]) -> str:
    if not citations:
        return "I could not find enough structured contract evidence to answer."
    primary = citations[0]
    lower = question.lower()
    if primary.kind == "table_row":
        return f"The relevant table row says: {primary.quote} [{primary.citation_id}]"
    if primary.kind == "metadata":
        return f"The structured metadata says: {primary.quote} [{primary.citation_id}]"
    if "excluded" in lower and len(citations) > 1:
        return " ".join(f"{citation.quote} [{citation.citation_id}]" for citation in citations[:2])
    return f"{primary.quote} [{primary.citation_id}]"
