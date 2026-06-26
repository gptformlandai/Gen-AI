from __future__ import annotations

from semantic_search_lab.schemas import Document


TOPICS = [
    {
        "topic": "password_reset",
        "product": "identity",
        "doc_type": "how_to",
        "audience": "employees",
        "title": "Reset Password And Account Recovery",
        "body": "Users who forget a password can reset credentials from the login page. The recovery flow verifies identity with MFA, sends a one time code, and records account recovery status for help desk review.",
    },
    {
        "topic": "vendor_onboarding",
        "product": "procurement",
        "doc_type": "workflow",
        "audience": "managers",
        "title": "Vendor Onboarding Approval Workflow",
        "body": "Employees submit supplier details, managers approve or reject the vendor request, and finance verifies tax information. Requesters receive notifications when approval status changes.",
    },
    {
        "topic": "support_dashboard",
        "product": "support",
        "doc_type": "dashboard",
        "audience": "support_leads",
        "title": "Support Ticket SLA Dashboard",
        "body": "Support leads review ticket volume, SLA breaches, top categories, aging queues, and weekly trends. The dashboard helps teams identify operational bottlenecks and export support metrics.",
    },
    {
        "topic": "appointment_reminders",
        "product": "healthcare",
        "doc_type": "workflow",
        "audience": "customers",
        "title": "Appointment Reminder Notifications",
        "body": "Patients receive email and SMS appointment reminders twenty four hours before a visit. The system supports opt out preferences, delivery status logs, and operations follow up.",
    },
    {
        "topic": "knowledge_review",
        "product": "knowledge_base",
        "doc_type": "how_to",
        "audience": "employees",
        "title": "Knowledge Article Review Process",
        "body": "Employees search knowledge articles, filter by department, inspect the last reviewed date, and flag outdated content. Content owners receive review tasks for stale articles.",
    },
    {
        "topic": "csv_reconciliation",
        "product": "finance",
        "doc_type": "workflow",
        "audience": "analysts",
        "title": "CSV Transaction Reconciliation",
        "body": "Finance analysts upload two CSV files, match transactions by identifier and amount, highlight mismatches, and download an exception report for unresolved reconciliation items.",
    },
    {
        "topic": "role_based_access",
        "product": "admin",
        "doc_type": "policy",
        "audience": "admins",
        "title": "Role Based Access For Content Review",
        "body": "Admins manage user roles for administrators, reviewers, and read only users. Reviewers approve content changes while read only users can view published records only.",
    },
    {
        "topic": "new_hire_onboarding",
        "product": "hr",
        "doc_type": "workflow",
        "audience": "hr",
        "title": "New Hire Onboarding Checklist",
        "body": "HR assigns onboarding tasks to new hires, employees mark tasks complete, managers track progress, and overdue checklist items trigger reminder notifications.",
    },
    {
        "topic": "report_exports",
        "product": "analytics",
        "doc_type": "reference",
        "audience": "analysts",
        "title": "Report Export Reference",
        "body": "Users export analytics reports as CSV files, choose a date range, filter rows by status, and download data for offline analysis or monthly business review.",
    },
    {
        "topic": "audit_trail",
        "product": "compliance",
        "doc_type": "policy",
        "audience": "auditors",
        "title": "Audit Trail And Change History",
        "body": "The platform records important user actions, status changes, approvals, rejections, and administrative updates. Audit history supports compliance review and incident investigation.",
    },
    {
        "topic": "incident_triage",
        "product": "operations",
        "doc_type": "runbook",
        "audience": "operators",
        "title": "Incident Triage Runbook",
        "body": "Operators classify incidents by severity, assign an owner, record timeline updates, notify stakeholders, and close incidents after the recovery action is verified.",
    },
    {
        "topic": "billing_disputes",
        "product": "billing",
        "doc_type": "workflow",
        "audience": "customers",
        "title": "Billing Dispute Workflow",
        "body": "Customers open billing disputes for unexpected charges. Agents review invoice details, request supporting evidence, update dispute status, and issue refunds when approved.",
    },
]


REGIONS = ["global", "us", "eu", "apac"]
DEPARTMENTS = ["operations", "finance", "support", "hr", "security"]


def build_sample_documents(count: int = 360) -> list[Document]:
    """Create a repeatable non-trivial corpus.

    The generated corpus is template-based on purpose: it gives us enough scale
    to compare retrieval modes while keeping labels and metadata predictable.
    """

    documents: list[Document] = []
    for index in range(count):
        topic = TOPICS[index % len(TOPICS)]
        variant = index // len(TOPICS) + 1
        region = REGIONS[index % len(REGIONS)]
        department = DEPARTMENTS[index % len(DEPARTMENTS)]
        document_id = f"{topic['topic']}-{variant:03d}-{region}"
        title = f"{topic['title']} Variant {variant:03d}"
        text = (
            f"{topic['body']} "
            f"This variant applies to the {region} region and the {department} department. "
            f"Operational notes include clear ownership, traceable status, searchable metadata, and escalation guidance. "
            f"Document topic marker: {topic['topic']}."
        )
        documents.append(
            Document(
                id=document_id,
                title=title,
                text=text,
                metadata={
                    "topic": topic["topic"],
                    "product": topic["product"],
                    "doc_type": topic["doc_type"],
                    "audience": topic["audience"],
                    "region": region,
                    "department": department,
                },
            )
        )
    return documents
