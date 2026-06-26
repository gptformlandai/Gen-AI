# Short Safety Policy

The assistant follows two guardrail layers before retrieval:

1. **Safety refusal:** refuse requests about bypassing authentication, stealing credentials, disabling audit logs, or hiding user actions.
2. **Permission refusal:** refuse audit-trail and admin role-management details unless the user role is authorized.

## Allowed Roles

- Audit-trail details: `auditor`, `admin`, `security`, `compliance`
- Role-management details: `admin`, `security`

## Response Behavior

When a guardrail blocks a request, the assistant returns:

- status: `refused`
- no citations
- a short refusal reason
- low confidence

The system does not retrieve context for blocked requests. This avoids leaking sensitive details through citations.
