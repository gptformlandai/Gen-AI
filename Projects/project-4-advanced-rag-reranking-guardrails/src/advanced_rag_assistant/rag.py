from __future__ import annotations

from advanced_rag_assistant.chunking import split_sentences, tokenize
from advanced_rag_assistant.guardrails import GuardrailEngine
from advanced_rag_assistant.query_rewriting import QueryRewriter
from advanced_rag_assistant.reranking import STOPWORDS, CandidateReranker
from advanced_rag_assistant.schemas import Citation, RagAnswer, RerankedHit, SearchHit
from advanced_rag_assistant.vector_store import InMemoryVectorStore


class BaselineRagAssistant:
    """Project 3-style baseline for side-by-side comparison."""

    def __init__(self, store: InMemoryVectorStore, min_top_score: float = 0.06) -> None:
        self.store = store
        self.min_top_score = min_top_score

    def answer(self, question: str, user_role: str = "employee") -> RagAnswer:
        if self._is_unsafe(question):
            return self._refuse(question, user_role, "The question asks for unsafe credential or control-bypass behavior.")
        hits = self.store.search(question, k=5)
        if not hits or hits[0].score < self.min_top_score:
            return self._refuse(question, user_role, "Retrieved evidence was missing or below the confidence threshold.")
        citations = self._citations_from_hits(hits[:3])
        return RagAnswer(
            question=question,
            user_role=user_role,
            status="answered",
            answer=self._answer_from_citations(citations),
            citations=citations,
            confidence="medium",
        )

    def _is_unsafe(self, question: str) -> bool:
        lower = question.lower()
        return "bypass login" in lower or "bypass authentication" in lower or "steal password" in lower

    def _citations_from_hits(self, hits: list[SearchHit]) -> list[Citation]:
        citations: list[Citation] = []
        seen: set[str] = set()
        for hit in hits:
            quote = core_quote(hit.text)
            if quote in seen:
                continue
            seen.add(quote)
            citations.append(
                Citation(
                    citation_id=f"S{len(citations) + 1}",
                    document_id=hit.document_id,
                    chunk_id=hit.chunk_id,
                    title=hit.title,
                    quote=quote,
                    score=hit.score,
                    rerank_score=hit.score,
                    metadata=hit.metadata,
                )
            )
            if len(citations) == 2:
                break
        return citations

    def _answer_from_citations(self, citations: list[Citation]) -> str:
        return " ".join(f"{citation.quote} [{citation.citation_id}]" for citation in citations[:1])

    def _refuse(self, question: str, user_role: str, reason: str) -> RagAnswer:
        return RagAnswer(
            question=question,
            user_role=user_role,
            status="refused",
            answer="I do not have enough allowed evidence to answer that question reliably.",
            citations=[],
            refusal_reason=reason,
            confidence="low",
        )


class AdvancedRagAssistant:
    """Advanced RAG pipeline with guardrails, multi-query retrieval, and reranking."""

    def __init__(
        self,
        store: InMemoryVectorStore,
        min_rerank_score: float = 0.22,
        guardrails: GuardrailEngine | None = None,
        rewriter: QueryRewriter | None = None,
        reranker: CandidateReranker | None = None,
    ) -> None:
        self.store = store
        self.min_rerank_score = min_rerank_score
        self.guardrails = guardrails or GuardrailEngine()
        self.rewriter = rewriter or QueryRewriter()
        self.reranker = reranker or CandidateReranker()

    def answer(self, question: str, user_role: str = "employee") -> RagAnswer:
        decision = self.guardrails.check(question, user_role)
        if not decision.allowed:
            return self._refuse(question, user_role, decision.reason)

        variants = self.rewriter.rewrite(question)
        candidates, query_map = self._retrieve_candidates(variants)
        reranked = self.reranker.rerank(question, candidates, query_map)

        if not reranked or reranked[0].rerank_score < self.min_rerank_score:
            return self._refuse(
                question,
                user_role,
                "Retrieved and reranked evidence was below the confidence threshold.",
            )

        citations = self._build_citations(reranked[:4])
        return RagAnswer(
            question=question,
            user_role=user_role,
            status="answered",
            answer=" ".join(f"{citation.quote} [{citation.citation_id}]" for citation in citations[:1]),
            citations=citations,
            confidence="high" if reranked[0].rerank_score >= 0.8 else "medium",
        )

    def _retrieve_candidates(self, queries: list[str]) -> tuple[list[SearchHit], dict[str, list[str]]]:
        by_chunk_id: dict[str, SearchHit] = {}
        query_map: dict[str, list[str]] = {}
        for query in queries:
            for hit in self.store.search(query, k=8):
                current = by_chunk_id.get(hit.chunk_id)
                if current is None or hit.score > current.score:
                    by_chunk_id[hit.chunk_id] = hit
                query_map.setdefault(hit.chunk_id, []).append(query)
        return list(by_chunk_id.values()), query_map

    def _build_citations(self, hits: list[RerankedHit]) -> list[Citation]:
        citations: list[Citation] = []
        seen: set[str] = set()
        for hit in hits:
            quote = core_quote(hit.text)
            if quote in seen:
                continue
            seen.add(quote)
            citations.append(
                Citation(
                    citation_id=f"S{len(citations) + 1}",
                    document_id=hit.document_id,
                    chunk_id=hit.chunk_id,
                    title=hit.title,
                    quote=quote,
                    score=hit.score,
                    rerank_score=hit.rerank_score,
                    metadata=hit.metadata,
                )
            )
            if len(citations) == 3:
                break
        return citations

    def _refuse(self, question: str, user_role: str, reason: str) -> RagAnswer:
        return RagAnswer(
            question=question,
            user_role=user_role,
            status="refused",
            answer="I cannot answer that from allowed retrieved evidence.",
            citations=[],
            refusal_reason=reason,
            confidence="low",
        )


def core_quote(text: str) -> str:
    """Keep only source facts and skip generated boilerplate."""

    selected: list[str] = []
    for sentence in split_sentences(text):
        if sentence.startswith(("This article applies", "Operational guidance", "Topic marker")):
            continue
        selected.append(sentence)
        if len(selected) == 2:
            break
    return " ".join(selected) if selected else text


def query_overlap(question: str, text: str) -> int:
    return len((set(tokenize(question)) - STOPWORDS) & set(tokenize(text)))
