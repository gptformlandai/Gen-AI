from __future__ import annotations

from time import perf_counter

from mcp_change_workflow.schemas import BudgetEstimate


class BudgetTracker:
    """Track request, token, cost, and latency budget for one workflow run."""

    def __init__(self, latency_budget_ms: float = 500.0, request_budget: int = 4) -> None:
        self.started_at = perf_counter()
        self.estimated_tokens = 0
        self.mcp_request_count = 0
        self.latency_budget_ms = latency_budget_ms
        self.request_budget = request_budget

    def record_boundary_call(self, text_payload: str) -> None:
        self.mcp_request_count += 1
        self.estimated_tokens += estimate_tokens(text_payload)

    def snapshot(self) -> BudgetEstimate:
        latency_ms = (perf_counter() - self.started_at) * 1000
        estimated_cost = round(self.estimated_tokens * 0.000002, 8)
        return BudgetEstimate(
            estimated_tokens=self.estimated_tokens,
            estimated_cost_usd=estimated_cost,
            mcp_request_count=self.mcp_request_count,
            measured_latency_ms=round(latency_ms, 3),
            latency_budget_ms=self.latency_budget_ms,
            request_budget=self.request_budget,
            within_latency_budget=latency_ms <= self.latency_budget_ms,
            within_request_budget=self.mcp_request_count <= self.request_budget,
        )


def estimate_tokens(text: str) -> int:
    """Simple deterministic token estimate for budget practice."""

    words = [word for word in text.replace("\n", " ").split(" ") if word]
    return max(1, int(len(words) * 1.3))
