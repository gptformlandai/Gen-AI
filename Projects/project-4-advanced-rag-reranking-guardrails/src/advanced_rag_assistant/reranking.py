from __future__ import annotations

from advanced_rag_assistant.chunking import tokenize
from advanced_rag_assistant.schemas import RerankedHit, SearchHit


STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "do", "does", "for", "from",
    "how", "in", "is", "it", "of", "on", "or", "the", "to", "what", "when", "where", "who",
    "with", "which",
}

TOPIC_PROFILES = {
    "report_exports": {"export", "analytics", "reports", "csv", "date", "range", "download"},
    "incident_triage": {"incident", "triage", "severity", "owner", "stakeholders", "recovery"},
    "audit_trail": {"audit", "trail", "actions", "status", "approvals", "rejections", "administrative"},
    "role_based_access": {"roles", "admins", "reviewers", "read", "only", "published", "records"},
    "support_dashboard": {"dashboard", "ticket", "sla", "categories", "bottlenecks"},
    "knowledge_review": {"knowledge", "articles", "department", "reviewed", "stale", "outdated"},
}


class CandidateReranker:
    """Rerank retrieval candidates with transparent intent features."""

    def rerank(self, question: str, candidates: list[SearchHit], query_map: dict[str, list[str]]) -> list[RerankedHit]:
        question_tokens = set(tokenize(question)) - STOPWORDS
        reranked: list[RerankedHit] = []
        for hit in candidates:
            hit_tokens = set(tokenize(hit.text))
            lexical_overlap = len(question_tokens & hit_tokens) / max(len(question_tokens), 1)
            topic = hit.metadata.get("topic", "")
            topic_boost = self._topic_boost(question_tokens, topic)
            phrase_boost = self._phrase_boost(question.lower(), topic)
            rerank_score = hit.score + lexical_overlap + topic_boost + phrase_boost
            reason = (
                f"vector={hit.score:.3f}, overlap={lexical_overlap:.3f}, "
                f"topic_boost={topic_boost:.3f}, phrase_boost={phrase_boost:.3f}"
            )
            reranked.append(
                RerankedHit(
                    **hit.model_dump(),
                    rerank_score=round(rerank_score, 6),
                    retrieval_queries=query_map.get(hit.chunk_id, []),
                    rerank_reason=reason,
                )
            )
        reranked.sort(key=lambda hit: hit.rerank_score, reverse=True)
        return reranked

    def _topic_boost(self, question_tokens: set[str], topic: str) -> float:
        profile = TOPIC_PROFILES.get(topic, set())
        if not profile:
            return 0.0
        return min(len(question_tokens & profile) * 0.18, 0.72)

    def _phrase_boost(self, question: str, topic: str) -> float:
        if topic == "report_exports" and ("export options" in question or "analytics reports" in question):
            return 0.55
        if topic == "incident_triage" and ("triage" in question or "incident" in question):
            return 0.75
        if topic == "audit_trail" and ("audit trail" in question or "user actions" in question):
            return 0.45
        return 0.0
