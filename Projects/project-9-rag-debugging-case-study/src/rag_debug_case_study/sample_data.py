from __future__ import annotations

from rag_debug_case_study.schemas import KnowledgeDocument


DOCUMENTS = [
    KnowledgeDocument(
        doc_id="admin_permissions",
        title="Operator and administrator permissions",
        body=(
            "Operators can view dashboards and audit logs. Administrators can invite users, "
            "update roles, and revoke access tokens. Incident dashboard access is read-only."
        ),
        tags=["operators", "admin", "permissions"],
    ),
    KnowledgeDocument(
        doc_id="password_reset",
        title="Password reset runbook",
        body=(
            "Users reset forgotten passwords from Sign-in > Forgot password. Admins can send a reset link "
            "from Identity > Users. Reset links expire after 15 minutes and require MFA."
        ),
        tags=["identity", "password", "mfa"],
    ),
    KnowledgeDocument(
        doc_id="analytics_export",
        title="Analytics export options",
        body=(
            "Reports may be saved as CSV or PDF. Scheduled exports can email recipients daily or weekly. "
            "Large report files are prepared asynchronously in the export center."
        ),
        tags=["analytics", "export", "reports", "scheduled"],
    ),
    KnowledgeDocument(
        doc_id="incident_response",
        title="Incident response triage",
        body=(
            "Alert response starts by acknowledging the page, classifying severity, assigning an incident "
            "commander, checking recent deployments, and creating a mitigation task. SEV1 outages require "
            "immediate escalation."
        ),
        tags=["incident", "triage", "operations", "mitigation"],
    ),
    KnowledgeDocument(
        doc_id="api_errors",
        title="API error handling",
        body=(
            "Failed API calls return structured JSON errors with code, message, and request id. Clients should "
            "log the request id before contacting support."
        ),
        tags=["api", "errors", "failed calls"],
    ),
    KnowledgeDocument(
        doc_id="webhook_delivery",
        title="Webhook delivery verification and retry policy",
        body=(
            "Webhook delivery retries use exponential backoff for 24 hours. Each request includes an HMAC "
            "signature header and a delivery id so receivers can verify authenticity."
        ),
        tags=["webhook", "retry", "signature", "verification"],
    ),
    KnowledgeDocument(
        doc_id="account_access",
        title="Account access changes",
        body=(
            "Account owners can remove team members from workspace access. Removed users lose access "
            "immediately but their audit events remain visible."
        ),
        tags=["account", "access", "remove users"],
    ),
    KnowledgeDocument(
        doc_id="data_deletion",
        title="Data deletion after account closure",
        body=(
            "After account closure, personal data enters a 30 day retention period before deletion unless a "
            "legal hold applies. The deletion job records completion in the privacy ledger."
        ),
        tags=["privacy", "deletion", "retention", "account data"],
    ),
    KnowledgeDocument(
        doc_id="sso_setup",
        title="Single sign-on setup",
        body=(
            "Single sign-on supports SAML and OIDC. Enforce domain verification before enabling SSO. "
            "Test with a pilot group before company-wide rollout."
        ),
        tags=["sso", "saml", "oidc", "identity"],
    ),
    KnowledgeDocument(
        doc_id="cache_ttl",
        title="Search cache TTL",
        body=(
            "Search result cache entries expire after 10 minutes. The service uses stale-while-revalidate "
            "for popular queries so users can receive a fast cached response while refresh runs."
        ),
        tags=["cache", "ttl", "search"],
    ),
    KnowledgeDocument(
        doc_id="rate_limits",
        title="API rate limits and throttling",
        body=(
            "API clients are limited to 600 requests per minute. When the limit is exceeded, responses include "
            "HTTP 429 and a Retry-After header."
        ),
        tags=["api", "rate limit", "throttle", "429"],
    ),
    KnowledgeDocument(
        doc_id="refunds",
        title="Refund policy",
        body=(
            "Refunds are available for duplicate charges within 30 days. Subscription cancellations take effect "
            "at the end of the billing period."
        ),
        tags=["billing", "refund", "duplicate charges"],
    ),
    KnowledgeDocument(
        doc_id="audit_export",
        title="Audit log export",
        body=(
            "Audit logs can be filtered by actor, action, and date. Compliance administrators can export "
            "immutable CSV audit reports for regulatory review."
        ),
        tags=["audit", "compliance", "export"],
    ),
    KnowledgeDocument(
        doc_id="mobile_offline",
        title="Mobile offline draft behavior",
        body=(
            "The mobile app supports offline drafts. Changes sync when connectivity returns; conflicts are "
            "resolved by the latest server version."
        ),
        tags=["mobile", "offline", "sync"],
    ),
]

