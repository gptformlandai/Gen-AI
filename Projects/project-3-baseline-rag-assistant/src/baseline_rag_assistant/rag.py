from __future__ import annotations

from baseline_rag_assistant.chunking import split_sentences, tokenize
from baseline_rag_assistant.prompts import build_evidence_packet
from baseline_rag_assistant.schemas import Citation, RagAnswer, SearchHit
from baseline_rag_assistant.tracing import JsonlTraceLogger
from baseline_rag_assistant.vector_store import InMemoryVectorStore


RISKY_PATTERNS = ("bypass login", "bypass authentication", "steal password", "steal credentials")


class BaselineRagAssistant:
    """Baseline RAG pipeline: retrieve, package evidence, answer or refuse."""

    def __init__(
        self,
        store: InMemoryVectorStore,
        min_top_score: float = 0.06,
        min_query_overlap: int = 1,
    ) -> None:
        self.store = store
        self.min_top_score = min_top_score
        self.min_query_overlap = min_query_overlap

    def answer(
        self,
        question: str,
        k: int = 5,
        trace_logger: JsonlTraceLogger | None = None,
    ) -> RagAnswer:
        logger = trace_logger or JsonlTraceLogger()
        logger.log("question_received", {"question": question, "k": k})

        if self._is_risky(question):
            logger.log("refusal", {"reason": "safety_policy"})
            return RagAnswer(
                question=question,
                status="refused",
                answer="I do not have safe support documentation that can answer that request.",
                citations=[],
                refusal_reason="The question asks for bypassing access controls or credential abuse.",
                confidence="low",
            )

        hits = self.store.search(question, k=k)
        logger.log(
            "retrieval",
            {
                "hits": [
                    {
                        "chunk_id": hit.chunk_id,
                        "score": hit.score,
                        "topic": hit.metadata.get("topic", ""),
                    }
                    for hit in hits
                ]
            },
        )

        if not self._has_enough_evidence(question, hits):
            logger.log(
                "refusal",
                {
                    "reason": "insufficient_evidence",
                    "top_score": hits[0].score if hits else 0.0,
                },
            )
            return RagAnswer(
                question=question,
                status="refused",
                answer="I do not have enough retrieved evidence to answer that question reliably.",
                citations=[],
                refusal_reason="Retrieved evidence was missing or below the confidence threshold.",
                confidence="low",
            )

        citations = self._build_citations(question, hits[:3])
        evidence_packet = build_evidence_packet(question, citations)
        logger.log("evidence_packet_built", {"evidence_packet": evidence_packet})

        answer_text = self._synthesize_answer(question, citations)
        logger.log(
            "answer_finalized",
            {
                "status": "answered",
                "citation_ids": [citation.citation_id for citation in citations],
            },
        )
        return RagAnswer(
            question=question,
            status="answered",
            answer=answer_text,
            citations=citations,
            confidence="medium" if hits[0].score < 0.35 else "high",
        )

    def _has_enough_evidence(self, question: str, hits: list[SearchHit]) -> bool:
        if not hits or hits[0].score < self.min_top_score:
            return False
        query_tokens = set(tokenize(question)) - STOPWORDS
        top_tokens = set(tokenize(" ".join(hit.text for hit in hits[:3])))
        return len(query_tokens & top_tokens) >= self.min_query_overlap

    def _build_citations(self, question: str, hits: list[SearchHit]) -> list[Citation]:
        citations: list[Citation] = []
        seen_quotes: set[str] = set()
        for hit in hits:
            quote = self._best_sentence(question, hit.text)
            if quote in seen_quotes:
                continue
            seen_quotes.add(quote)
            citations.append(
                Citation(
                    citation_id=f"S{len(citations) + 1}",
                    document_id=hit.document_id,
                    chunk_id=hit.chunk_id,
                    title=hit.title,
                    quote=quote,
                    score=hit.score,
                    metadata=hit.metadata,
                )
            )
            if len(citations) == 3:
                break
        return citations

    def _synthesize_answer(self, question: str, citations: list[Citation]) -> str:
        """Extractive synthesis keeps claims tied to retrieved evidence."""

        answer_sentences = []
        for citation in citations[:2]:
            answer_sentences.append(f"{citation.quote} [{citation.citation_id}]")
        return " ".join(answer_sentences)

    def _best_sentence(self, question: str, text: str) -> str:
        core_sentences = self._core_evidence_sentences(text)
        if core_sentences:
            return " ".join(core_sentences)

        question_tokens = set(tokenize(question)) - STOPWORDS
        best_sentence = split_sentences(text)[0] if split_sentences(text) else text
        best_overlap = -1
        for sentence in split_sentences(text):
            overlap = len(question_tokens & set(tokenize(sentence)))
            if overlap > best_overlap:
                best_sentence = sentence
                best_overlap = overlap
        return best_sentence

    def _core_evidence_sentences(self, text: str) -> list[str]:
        """Keep the topic facts and remove generated operational boilerplate."""

        selected: list[str] = []
        for sentence in split_sentences(text):
            if sentence.startswith(("This article applies", "Operational guidance", "Topic marker")):
                continue
            selected.append(sentence)
            if len(selected) == 2:
                break
        return selected

    def _is_risky(self, question: str) -> bool:
        lower = question.lower()
        return any(pattern in lower for pattern in RISKY_PATTERNS)


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "can",
    "do",
    "does",
    "for",
    "from",
    "how",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "the",
    "to",
    "what",
    "when",
    "where",
    "who",
    "with",
}
