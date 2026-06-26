from __future__ import annotations


class QueryRewriter:
    """Rule-based multi-query expansion for visible retrieval engineering."""

    def rewrite(self, question: str) -> list[str]:
        lower = question.lower()
        queries = [question]

        if "export" in lower or "analytics report" in lower:
            queries.append("users export analytics reports csv files choose date range download data")
        if "incident" in lower or "triage" in lower:
            queries.append("operators classify incidents by severity assign owner notify stakeholders recovery action verified")
        if "audit" in lower or "user actions" in lower:
            queries.append("audit trail records user actions status changes approvals rejections administrative updates")
        if "role" in lower or "read only" in lower:
            queries.append("admins manage user roles administrators reviewers read only users view published records")
        if "password" in lower or "login" in lower:
            queries.append("forgot password reset credentials login recovery mfa one time code")

        # Preserve order while removing duplicates.
        deduped: list[str] = []
        for query in queries:
            if query not in deduped:
                deduped.append(query)
        return deduped
