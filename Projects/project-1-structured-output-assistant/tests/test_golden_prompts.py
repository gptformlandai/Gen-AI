from __future__ import annotations

import json
from pathlib import Path

from structured_output_assistant.llm import RuleBasedRequirementsModel
from structured_output_assistant.workflow import run_requirements_assistant


GOLDEN_PROMPTS = Path(__file__).resolve().parents[1] / "data" / "golden_prompts.json"


def test_golden_prompts_return_expected_statuses() -> None:
    prompts = json.loads(GOLDEN_PROMPTS.read_text(encoding="utf-8"))

    for prompt in prompts:
        result = run_requirements_assistant(
            prompt["input"],
            model=RuleBasedRequirementsModel(),
            max_retries=1,
        )

        assert result.status == prompt["expected_status"], prompt["id"]
        assert result.output is not None, prompt["id"]
        assert result.errors == [], prompt["id"]


def test_golden_set_has_at_least_ten_prompts() -> None:
    prompts = json.loads(GOLDEN_PROMPTS.read_text(encoding="utf-8"))

    assert len(prompts) >= 10
