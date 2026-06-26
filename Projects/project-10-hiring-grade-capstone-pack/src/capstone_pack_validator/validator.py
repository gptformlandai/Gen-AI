from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AssetCheck:
    path: str
    exists: bool
    missing_phrases: list[str]

    @property
    def passed(self) -> bool:
        return self.exists and not self.missing_phrases


@dataclass(frozen=True)
class ValidationReport:
    checks: list[AssetCheck]

    @property
    def passed(self) -> bool:
        return all(check.passed for check in self.checks)

    def to_markdown(self) -> str:
        lines = [
            "# Capstone Pack Validation",
            "",
            "| Asset | Passed | Missing phrases |",
            "|---|---:|---|",
        ]
        for check in self.checks:
            lines.append(
                f"| {check.path} | {check.passed} | {', '.join(check.missing_phrases) or 'none'} |"
            )
        return "\n".join(lines) + "\n"


def validate_pack(root: Path) -> ValidationReport:
    manifest = json.loads((root / "data" / "asset_manifest.json").read_text(encoding="utf-8"))
    checks: list[AssetCheck] = []
    for asset in manifest["required_assets"]:
        relative_path = asset["path"]
        path = root / relative_path
        if not path.exists():
            checks.append(AssetCheck(path=relative_path, exists=False, missing_phrases=asset["required_phrases"]))
            continue
        text = path.read_text(encoding="utf-8")
        missing = [phrase for phrase in asset["required_phrases"] if phrase not in text]
        checks.append(AssetCheck(path=relative_path, exists=True, missing_phrases=missing))
    return ValidationReport(checks=checks)

