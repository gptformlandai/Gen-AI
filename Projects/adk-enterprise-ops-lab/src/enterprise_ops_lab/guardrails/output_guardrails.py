from __future__ import annotations


def validate_output(text: str, confidence: float, threshold: float = 0.72) -> tuple[bool, str]:
    if confidence < threshold:
        return False, "confidence below threshold; escalate to human"
    if "secret" in text.lower():
        return False, "output may contain sensitive content"
    return True, "output accepted"

