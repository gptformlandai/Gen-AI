"""Deterministic local embedding service.

This is intentionally simple so tests and demos run offline. Production swaps it
for provider embeddings and stores vectors in a vector database.
"""

from __future__ import annotations

import hashlib
import math
import re


class HashingEmbeddingService:
    def __init__(self, dimensions: int = 64) -> None:
        self.dimensions = dimensions

    def embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        for token in re.findall(r"[A-Za-z0-9_-]+", text.lower()):
            digest = hashlib.sha1(token.encode("utf-8")).hexdigest()
            index = int(digest[:8], 16) % self.dimensions
            vector[index] += 1.0
        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]


def cosine_similarity(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))
