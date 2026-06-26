from __future__ import annotations


INJECTION_MARKERS = ["ignore previous", "reveal system", "developer message", "exfiltrate", "bypass guardrail"]


def check_input(text: str) -> tuple[bool, str]:
    lower = text.lower()
    for marker in INJECTION_MARKERS:
        if marker in lower:
            return False, f"Blocked prompt-injection marker: {marker}"
    return True, "input accepted"

