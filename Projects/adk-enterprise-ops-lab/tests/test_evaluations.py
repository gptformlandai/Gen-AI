from pathlib import Path

from enterprise_ops_lab.evals.evaluation_runner import run_all_evaluations


def test_evaluations_run() -> None:
    root = Path(__file__).resolve().parents[1]
    results = run_all_evaluations(root)

    assert set(results) == {"golden", "trajectory", "rag_grounding"}
    assert results["rag_grounding"]["pass_rate"] >= 0.66

