"""Access control placeholder for production graph reads and writes."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AccessPolicy:
    allowed_roles: set[str] = field(default_factory=lambda: {"engineer", "sre", "architect"})

    def can_read(self, role: str, label: str) -> bool:
        return role in self.allowed_roles and label not in {"Owner"} or role == "architect"

    def can_write(self, role: str) -> bool:
        return role in {"sre", "architect"}
