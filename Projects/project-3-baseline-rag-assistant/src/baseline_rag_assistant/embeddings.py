from __future__ import annotations

import hashlib
import math
from collections import Counter

from baseline_rag_assistant.chunking import tokenize


SYNONYMS = {
    "forgotten": ["forgot", "reset", "recovery"],
    "password": ["credentials", "login"],
    "login": ["account", "identity"],
    "supplier": ["vendor"],
    "vendor": ["supplier"],
    "approve": ["approval", "review"],
    "approves": ["approval", "review"],
    "approved": ["approval"],
    "metrics": ["dashboard", "volume"],
    "options": ["reference", "available"],
    "ticket": ["support", "case"],
    "sla": ["breach", "support"],
    "reminders": ["notification", "notify"],
    "reminder": ["notification", "notify"],
    "notify": ["notification", "reminder"],
    "outdated": ["stale", "review"],
    "stale": ["outdated", "review"],
    "article": ["knowledge", "content"],
    "csv": ["export", "file"],
    "mismatches": ["exception", "reconciliation"],
    "mismatched": ["exception", "reconciliation"],
    "transactions": ["payment", "finance"],
    "roles": ["access", "permission"],
    "role": ["access", "permission"],
    "overdue": ["late", "reminder"],
    "download": ["export"],
    "incident": ["triage", "severity"],
    "triage": ["incident", "severity"],
    "audit": ["history", "compliance"],
    "vacation": ["holiday", "pto"],
}


class HashingTfidfEmbeddingModel:
    """Deterministic embedding model for local RAG experiments."""

    def __init__(self, dimensions: int = 256) -> None:
        self.dimensions = dimensions
        self.idf: dict[str, float] = {}
        self.default_idf = 1.0

    def fit(self, texts: list[str]) -> None:
        document_frequency: Counter[str] = Counter()
        for text in texts:
            document_frequency.update(set(self._expanded_tokens(text)))
        total = max(len(texts), 1)
        self.idf = {
            token: math.log((1 + total) / (1 + frequency)) + 1.0
            for token, frequency in document_frequency.items()
        }
        self.default_idf = math.log((1 + total) / 1) + 1.0

    def embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        term_frequency = Counter(self._expanded_tokens(text))
        for token, frequency in term_frequency.items():
            vector[self._hash_index(token)] += self._hash_sign(token) * frequency * self.idf.get(
                token, self.default_idf
            )
        return self._normalize(vector)

    def embed_many(self, texts: list[str]) -> list[list[float]]:
        return [self.embed(text) for text in texts]

    def _expanded_tokens(self, text: str) -> list[str]:
        expanded: list[str] = []
        for token in tokenize(text):
            expanded.append(token)
            expanded.extend(SYNONYMS.get(token, []))
        return expanded

    def _hash_index(self, token: str) -> int:
        digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
        return int(digest[:8], 16) % self.dimensions

    def _hash_sign(self, token: str) -> int:
        digest = hashlib.sha256(f"sign:{token}".encode("utf-8")).hexdigest()
        return 1 if int(digest[:2], 16) % 2 == 0 else -1

    def _normalize(self, vector: list[float]) -> list[float]:
        magnitude = math.sqrt(sum(value * value for value in vector))
        if magnitude == 0:
            return vector
        return [value / magnitude for value in vector]


def cosine_similarity(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))
