"""Simplified RDF triple-store abstraction for local SPARQL examples."""

from __future__ import annotations

from dataclasses import dataclass, field


Triple = tuple[str, str, str]


@dataclass
class InMemoryTripleStore:
    triples: list[Triple] = field(default_factory=list)

    def add(self, subject: str, predicate: str, obj: str) -> None:
        triple = (subject, predicate, obj)
        if triple not in self.triples:
            self.triples.append(triple)

    def query_predicate(self, predicate: str) -> list[Triple]:
        return [triple for triple in self.triples if triple[1] == predicate]

    def query_subject(self, subject: str) -> list[Triple]:
        return [triple for triple in self.triples if triple[0] == subject]

    def to_turtle(self) -> str:
        lines = ["@prefix ent: <https://example.com/enterprise#> .", ""]
        for subject, predicate, obj in sorted(self.triples):
            lines.append(f"ent:{subject} ent:{predicate} ent:{obj} .")
        return "\n".join(lines)
