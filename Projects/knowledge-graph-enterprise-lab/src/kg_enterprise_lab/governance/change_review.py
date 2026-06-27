"""Graph change review records."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class GraphChangeReview:
    change_id: str
    summary: str
    proposed_by: str
    affected_nodes: list[str] = field(default_factory=list)
    approved: bool = False

    def approve(self) -> None:
        self.approved = True
