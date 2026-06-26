from __future__ import annotations

import re


EMAIL_PATTERN = re.compile(r"\b[\w.\-+]+@[\w.\-]+\.\w+\b")
TOKEN_PATTERN = re.compile(r"\b(?:sk|ya29|ghp)_[A-Za-z0-9_\-]{8,}\b")


def redact_sensitive_data(text: str) -> str:
    text = EMAIL_PATTERN.sub("[redacted-email]", text)
    return TOKEN_PATTERN.sub("[redacted-token]", text)

