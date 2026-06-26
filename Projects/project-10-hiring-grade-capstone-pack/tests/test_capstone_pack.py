from __future__ import annotations

import json
from pathlib import Path

from capstone_pack_validator.validator import validate_pack


ROOT = Path(__file__).resolve().parents[1]


def test_required_assets_are_present_and_complete() -> None:
    report = validate_pack(ROOT)

    assert report.passed, report.to_markdown()


def test_metrics_are_grounded_in_source_projects() -> None:
    metrics = json.loads((ROOT / "data" / "capstone_metrics.json").read_text(encoding="utf-8"))

    assert metrics["metrics"]["advanced_rag"]["baseline_pass_rate"] == 0.76
    assert metrics["metrics"]["advanced_rag"]["advanced_pass_rate"] == 1.0
    assert metrics["metrics"]["debugging_case_study"]["baseline_retrieval_failures"] == 5
    assert metrics["metrics"]["debugging_case_study"]["improved_retrieval_failures"] == 0


def test_resume_bullets_are_limited_and_measurable() -> None:
    text = (ROOT / "docs" / "resume_bullets.md").read_text(encoding="utf-8")
    bullets = [line for line in text.splitlines() if line.startswith("- ")]

    assert 3 <= len(bullets) <= 5
    assert any("76.00%" in bullet and "100.00%" in bullet for bullet in bullets)
    assert any("retrieval failures" in bullet for bullet in bullets)


def test_demo_narrative_has_three_minute_structure() -> None:
    text = (ROOT / "docs" / "demo_narrative.md").read_text(encoding="utf-8")

    assert "## Minute 1" in text
    assert "## Minute 2" in text
    assert "## Minute 3" in text
