"""Sensitive data redaction helpers."""

from __future__ import annotations

import re


EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")


def redact_sensitive_text(text: str) -> str:
    return EMAIL_PATTERN.sub("[REDACTED_EMAIL]", text)
