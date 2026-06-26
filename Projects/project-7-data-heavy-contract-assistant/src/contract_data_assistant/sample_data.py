from __future__ import annotations


SAMPLE_DOCUMENTS = {
    "msa.md": """---
document_id: msa
title: Master Services Agreement
party_customer: Acme Health
party_vendor: Northstar AI
effective_date: 2026-01-15
governing_law: New York
---

# Master Services Agreement

## 1. Services
Vendor shall provide implementation, support, and analytics services described in each statement of work.
Customer shall provide timely access to systems and project stakeholders.

## 2. Confidentiality
Vendor shall protect Customer confidential information using reasonable safeguards.
Customer shall not disclose Vendor pricing or product roadmap information.
The confidentiality obligations survive termination for five years.

## 3. Fees and Payment
Customer shall pay undisputed invoices within 30 days.
Late payments may accrue interest at 1.5 percent per month.

## 4. Limitation of Liability
Each party's aggregate liability is capped at the fees paid in the 12 months before the claim.
The cap does not apply to confidentiality breaches, payment obligations, or willful misconduct.

## 5. Termination and Survival
Either party may terminate for material breach after 30 days written notice and failure to cure.
Confidentiality, payment obligations, and limitation of liability survive termination.

## 6. Governing Law
This Agreement is governed by the laws of New York.
""",
    "dpa.md": """---
document_id: dpa
title: Data Processing Addendum
customer_role: Data Controller
vendor_role: Data Processor
effective_date: 2026-01-15
governing_law: New York
---

# Data Processing Addendum

## 1. Roles
Customer acts as Data Controller and Vendor acts as Data Processor for personal data processed under the Agreement.

## 2. Processing Instructions
Vendor shall process personal data only on documented instructions from Customer.
Vendor shall ensure personnel are bound by confidentiality obligations.

## 3. Security Incident Notice
Vendor shall notify Customer of a confirmed security incident without undue delay and no later than 72 hours after confirmation.
The notice must describe known impact, affected systems, and mitigation actions.

## 4. Subprocessors
Vendor may use subprocessors listed in the approved subprocessor register.
Vendor shall provide 30 days advance notice before adding a new subprocessor.

## 5. Return or Deletion
After termination, Vendor shall delete or return personal data at Customer's choice unless law requires retention.
""",
    "sla.md": """---
document_id: sla
title: Service Level Agreement
service: Analytics Platform
measurement_window: monthly
support_hours: 24x7 for Severity 1
---

# Service Level Agreement

## 1. Availability Commitment
Vendor shall make the Analytics Platform available according to the service levels below.

| Uptime | Service Credit | Notes |
|---|---|---|
| >= 99.9% | 0% | Target service level |
| >= 99.5% and < 99.9% | 10% | Minor degradation |
| >= 99.0% and < 99.5% | 15% | Material degradation |
| < 99.0% | 25% | Severe degradation |

## 2. Support Response Times

| Severity | Description | Initial Response |
|---|---|---|
| Severity 1 | Production outage or critical data loss | 1 hour |
| Severity 2 | Major feature unavailable with workaround | 4 hours |
| Severity 3 | General question or minor defect | 1 business day |

## 3. Exclusions
Scheduled maintenance and Customer-caused outages do not count against uptime.
""",
}
