from __future__ import annotations

import itertools
import random
from collections import defaultdict

from semantic_search_lab.schemas import SearchHit
from semantic_search_lab.vector_store import InMemoryVectorStore, metadata_matches


class LSHApproximateIndex:
    """Random-hyperplane locality-sensitive hashing index.

    LSH turns each vector into a short binary signature. At query time we score
    only vectors in the same or nearby buckets. This is approximate because the
    best vector can live outside the inspected buckets.
    """

    def __init__(
        self,
        store: InMemoryVectorStore,
        num_planes: int = 6,
        seed: int = 42,
    ) -> None:
        self.store = store
        self.num_planes = num_planes
        self.seed = seed
        self.planes = self._build_planes()
        self.buckets: dict[str, list[int]] = defaultdict(list)
        self._index_vectors()

    def search(
        self,
        query: str,
        k: int = 5,
        filters: dict[str, str] | None = None,
        max_hamming_distance: int = 2,
        candidate_budget: int = 80,
        min_score_floor: float = 0.12,
    ) -> list[SearchHit]:
        query_vector = self.store.embedding_model.embed(query)
        signature = self._signature(query_vector)
        best_hits: list[SearchHit] = []
        for distance in range(max_hamming_distance, self.num_planes + 1):
            budget = len(self.store.chunks) if distance == self.num_planes else candidate_budget
            candidate_indices = self._candidate_indices(
                signature=signature,
                filters=filters,
                max_hamming_distance=distance,
                candidate_budget=budget,
            )
            if not candidate_indices:
                continue

            hits = self.store.search(query, k=k, filters=filters, candidate_indices=candidate_indices)
            if hits:
                best_hits = hits
            if hits and (hits[0].score >= min_score_floor or distance == self.num_planes):
                return hits

        return best_hits

    def _build_planes(self) -> list[list[float]]:
        rng = random.Random(self.seed)
        planes: list[list[float]] = []
        for _ in range(self.num_planes):
            plane = [rng.choice([-1.0, 1.0]) for _ in range(self.store.embedding_model.dimensions)]
            planes.append(plane)
        return planes

    def _index_vectors(self) -> None:
        for index, vector in enumerate(self.store.vectors):
            self.buckets[self._signature(vector)].append(index)

    def _signature(self, vector: list[float]) -> str:
        bits = []
        for plane in self.planes:
            dot = sum(value * plane_value for value, plane_value in zip(vector, plane))
            bits.append("1" if dot >= 0 else "0")
        return "".join(bits)

    def _candidate_indices(
        self,
        signature: str,
        filters: dict[str, str] | None,
        max_hamming_distance: int,
        candidate_budget: int,
    ) -> list[int]:
        candidates: list[int] = []
        for nearby_signature in self._nearby_signatures(signature, max_hamming_distance):
            for index in self.buckets.get(nearby_signature, []):
                chunk = self.store.chunks[index]
                if metadata_matches(chunk.metadata, filters):
                    candidates.append(index)
                if len(candidates) >= candidate_budget:
                    return candidates
        return candidates

    def _nearby_signatures(self, signature: str, max_hamming_distance: int) -> list[str]:
        signatures = [signature]
        positions = range(len(signature))
        for distance in range(1, max_hamming_distance + 1):
            for flips in itertools.combinations(positions, distance):
                bits = list(signature)
                for position in flips:
                    bits[position] = "0" if bits[position] == "1" else "1"
                signatures.append("".join(bits))
        return signatures
