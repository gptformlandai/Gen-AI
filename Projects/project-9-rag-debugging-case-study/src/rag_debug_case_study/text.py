from __future__ import annotations

import re


TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9]+")
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "before",
    "by",
    "can",
    "do",
    "for",
    "from",
    "how",
    "is",
    "of",
    "on",
    "or",
    "the",
    "to",
    "what",
    "when",
    "where",
    "which",
    "who",
    "with",
}

SYNONYMS = {
    "analytics": ["reports", "report"],
    "options": ["csv", "pdf", "scheduled", "email"],
    "triage": ["alert", "response", "severity", "commander", "mitigation"],
    "operators": ["operations", "oncall", "responder"],
    "incident": ["alert", "outage", "sev1"],
    "retried": ["retry", "retries", "backoff"],
    "verified": ["verify", "signature", "hmac", "authenticity"],
    "remove": ["deletion", "deleted", "closure", "retention"],
    "removed": ["deletion", "deleted", "closure", "retention"],
    "information": ["data", "personal"],
    "throttled": ["limit", "limited", "exceeded", "429", "retry-after"],
    "traffic": ["requests", "clients"],
    "ttl": ["expire", "expires", "minutes"],
    "single": ["sso"],
    "sign": ["sso"],
    "company": ["pilot", "rollout"],
    "wide": ["rollout"],
}


def tokenize(text: str, normalize: bool = False) -> list[str]:
    tokens = [token.lower() for token in TOKEN_PATTERN.findall(text)]
    if normalize:
        tokens = [normalize_token(token) for token in tokens]
    return [token for token in tokens if token and token not in STOPWORDS]


def normalize_token(token: str) -> str:
    if token.endswith("ies") and len(token) > 4:
        return f"{token[:-3]}y"
    if token.endswith("ed") and len(token) > 4:
        return token[:-2]
    if token.endswith("ing") and len(token) > 5:
        return token[:-3]
    if token.endswith("s") and len(token) > 4:
        return token[:-1]
    return token


def expand_query(text: str) -> str:
    tokens = tokenize(text, normalize=True)
    expanded = list(tokens)
    lower_text = text.lower()
    for token in tokens:
        expanded.extend(SYNONYMS.get(token, []))
    if "single sign-on" in lower_text:
        expanded.extend(["sso", "saml", "oidc"])
    if "company-wide" in lower_text:
        expanded.extend(["pilot", "domain", "verification", "rollout"])
    if "api traffic" in lower_text:
        expanded.extend(["rate", "limit", "600", "429", "retry-after"])
    return " ".join(expanded)

