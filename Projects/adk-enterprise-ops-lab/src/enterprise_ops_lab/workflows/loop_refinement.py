from __future__ import annotations


def refine_hypothesis(initial: str, evidence_terms: list[str], max_iterations: int = 3) -> list[str]:
    """Loop/refinement workflow that tightens a root-cause hypothesis."""
    hypotheses = [initial]
    current = initial
    for index, term in enumerate(evidence_terms[:max_iterations], start=1):
        current = f"{current} Evidence signal {index}: {term}."
        hypotheses.append(current)
    return hypotheses

