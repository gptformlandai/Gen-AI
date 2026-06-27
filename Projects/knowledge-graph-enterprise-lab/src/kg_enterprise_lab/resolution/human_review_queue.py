"""Human review queue for uncertain merges and low-confidence extraction."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class HumanReviewItem:
    id: str
    reason: str
    candidates: list[str]
    confidence: float


@dataclass
class HumanReviewQueue:
    items: list[HumanReviewItem] = field(default_factory=list)

    def add(self, item: HumanReviewItem) -> None:
        self.items.append(item)
