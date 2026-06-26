from __future__ import annotations

import math
import re
from collections import Counter


TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9\-]+")
STOPWORDS = {"a", "an", "and", "are", "as", "by", "for", "from", "in", "is", "of", "on", "or", "the", "to", "what", "with"}


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_PATTERN.findall(text) if token.lower() not in STOPWORDS]


def embed_text(text: str) -> dict[str, float]:
    counts = Counter(tokenize(text))
    norm = math.sqrt(sum(value * value for value in counts.values())) or 1.0
    return {token: count / norm for token, count in counts.items()}


def cosine(left: dict[str, float], right: dict[str, float]) -> float:
    return sum(left.get(token, 0.0) * right.get(token, 0.0) for token in set(left) | set(right))

