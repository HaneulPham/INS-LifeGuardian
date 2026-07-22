# Requirement review contract

Return these sections in this order for Jira stories, requirements, configuration changes, API changes, and technical remediation. Do not write detailed test cases.

## 1. Requirement Summary

Interpret the business and technical intent, current defect or limitation, expected behaviour, affected components, and behaviour that must remain unchanged. Do not merely restate the ticket.

## 2. Scope

Separate **In Scope**, **Out of Scope**, and **Conditional Scope / Open Questions**. Do not silently expand scope.

## 3. Missing Requirements and Gaps

Group as **Critical**, **Important**, and **Optional**. State what is missing, why it matters, and the safety, security, business, release, or test impact. Consider exact workflows, permissions, validation, null/empty/invalid/boundary input, errors, idempotency, retries, persistence, existing-data migration, compatibility, consumers, cross-platform behaviour, logs, deployment, and rollback.

## 4. Risk Analysis

Include only meaningful, evidence-supported risks. When useful, use High, Medium, Low, or Lowest. Cover consequence and affected consumers for safety, unauthorized access, tenant/data exposure, corruption or false persistence, missed or duplicate notifications, compatibility, platform inconsistency, deployment failure, jobs/queues, billing/reports, and observability.

## 5. Backend and Integration Impact

Address applicable routing, handlers/services, authentication, contracts, persistence, jobs/queues, CP, Portal, mobile, FCM, SMS, email, Twilio, QuickBooks, reports, logs, and Document Change Log. Explicitly state when a downstream integration must not trigger. Do not invent impacts.

## 6. Required Validations

Provide observable checks grouped where applicable as:

- Static and Configuration Validation
- Build and Packaging Validation
- Deployment Validation
- Runtime Functional Validation
- Data-Integrity Validation
- Integration and Observability Validation

Include positive/negative flows, authorization, generated infrastructure, persistence and false-persistence, duplicate prevention, downstream non-triggering, identifiers/correlation, privacy/sensitive-log checks, safe test recipients, test-data isolation, and cleanup or rollback when relevant. Mark unobservable primary behaviour as **Requires Test Instrumentation** and identify the exact evidence needed.

## 7. Questions

Group decision-ready questions as **Critical**, **Important**, and **Optional**. Ask only questions that resolve genuine ambiguities not answered by available evidence. Follow `question-decision-workflow.md`: one decision per question, two to five concrete behaviour options where practical, `Other – specify`, impact explanation, and a QA recommendation only when a safe default exists.

## 8. Proposed Test Coverage

Propose logical groups by feature, workflow stage, risk, platform, integration, or regression scope. For each group state its objective and risk reason. Stop before detailed rows.

## 9. Evidence and Assumptions

End with **Evidence Reviewed**, **Could Not Verify**, and **QA Assumptions**. Add **Source Conflicts** only when conflicts exist. For material behaviours whose source or status affects the result, include a compact traceability table: `Material Behaviour | Source / Evidence | Status`. Cite exact ticket content, files, routes, methods, fields, functions, tests, logs, or commands inspected.
