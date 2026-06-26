from __future__ import annotations

from advanced_rag_assistant.schemas import Document


TOPICS = [
    ("password_reset", "identity", "how_to", "employees", "Reset Password And Account Recovery", "Users who forget a password can reset credentials from the login page. The recovery flow verifies identity with MFA, sends a one time code, and records account recovery status for help desk review."),
    ("vendor_onboarding", "procurement", "workflow", "managers", "Vendor Onboarding Approval Workflow", "Employees submit supplier details, managers approve or reject the vendor request, and finance verifies tax information. Requesters receive notifications when approval status changes."),
    ("support_dashboard", "support", "dashboard", "support_leads", "Support Ticket SLA Dashboard", "Support leads review ticket volume, SLA breaches, top categories, aging queues, and weekly trends. The dashboard helps teams identify operational bottlenecks and export support metrics."),
    ("appointment_reminders", "healthcare", "workflow", "customers", "Appointment Reminder Notifications", "Patients receive email and SMS appointment reminders twenty four hours before a visit. The system supports opt out preferences, delivery status logs, and operations follow up."),
    ("knowledge_review", "knowledge_base", "how_to", "employees", "Knowledge Article Review Process", "Employees search knowledge articles, filter by department, inspect the last reviewed date, and flag outdated content. Content owners receive review tasks for stale articles."),
    ("csv_reconciliation", "finance", "workflow", "analysts", "CSV Transaction Reconciliation", "Finance analysts upload two CSV files, match transactions by identifier and amount, highlight mismatches, and download an exception report for unresolved reconciliation items."),
    ("role_based_access", "admin", "policy", "admins", "Role Based Access For Content Review", "Admins manage user roles for administrators, reviewers, and read only users. Reviewers approve content changes while read only users can view published records only."),
    ("new_hire_onboarding", "hr", "workflow", "hr", "New Hire Onboarding Checklist", "HR assigns onboarding tasks to new hires, employees mark tasks complete, managers track progress, and overdue checklist items trigger reminder notifications."),
    ("report_exports", "analytics", "reference", "analysts", "Report Export Reference", "Users export analytics reports as CSV files, choose a date range, filter rows by status, and download data for offline analysis or monthly business review."),
    ("audit_trail", "compliance", "policy", "auditors", "Audit Trail And Change History", "The platform records important user actions, status changes, approvals, rejections, and administrative updates. Audit history supports compliance review and incident investigation."),
    ("incident_triage", "operations", "runbook", "operators", "Incident Triage Runbook", "Operators classify incidents by severity, assign an owner, record timeline updates, notify stakeholders, and close incidents after the recovery action is verified."),
    ("billing_disputes", "billing", "workflow", "customers", "Billing Dispute Workflow", "Customers open billing disputes for unexpected charges. Agents review invoice details, request supporting evidence, update dispute status, and issue refunds when approved."),
]

REGIONS = ["global", "us", "eu", "apac"]
DEPARTMENTS = ["operations", "finance", "support", "hr", "security"]


def build_sample_documents(count: int = 240) -> list[Document]:
    documents: list[Document] = []
    for index in range(count):
        topic, product, doc_type, audience, title, body = TOPICS[index % len(TOPICS)]
        variant = index // len(TOPICS) + 1
        region = REGIONS[index % len(REGIONS)]
        department = DEPARTMENTS[index % len(DEPARTMENTS)]
        document_id = f"{topic}-{variant:03d}-{region}"
        text = (
            f"{body} "
            f"This article applies to the {region} region and the {department} department. "
            f"Operational guidance: use clear ownership, traceable status, searchable metadata, and escalation notes. "
            f"Topic marker: {topic}."
        )
        documents.append(
            Document(
                id=document_id,
                title=f"{title} Variant {variant:03d}",
                text=text,
                metadata={
                    "topic": topic,
                    "product": product,
                    "doc_type": doc_type,
                    "audience": audience,
                    "region": region,
                    "department": department,
                },
            )
        )
    return documents
