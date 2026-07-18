# INS LifeGuardian QA Second Brain Index

This folder is the durable supporting knowledge base for INS LifeGuardian QA.

Current Jira requirements, confirmed Jira comments, approved Confluence/API documentation, verified implementation evidence, and confirmed product behaviour take precedence over stored Second Brain knowledge.

When sources conflict, Codex must record the conflict and request clarification instead of silently selecting one behaviour.

## How Codex should use this knowledge

Before analyzing a ticket or writing test cases, Codex must check relevant files in this order:

1. `qa-knowledge/index.md`
2. `qa-knowledge/product/product-map.md`
3. Related module file under `qa-knowledge/product/modules/`
4. Existing ticket requirement under `qa-knowledge/requirements/`
5. Existing test cases under `qa-knowledge/test-cases/`
6. `qa-knowledge/regression/regression-map.md`
7. `qa-knowledge/decisions/decision-log.md`

Codex must not invent product behavior if the knowledge base does not contain it.
If behavior is missing, mark it as:
- Requirement gap
- QA assumption
- Question for BA/Dev

## Main Product Areas

- Billing
- Reports
- Care Plan Tasks
- Welfare Check
- Alerts/Restorals
- Emergency Alarm
- Notifications
- Device Setup/Checklist
- Service Requests/Work Orders
- Assets/Devices
- Client File
- Village inheritance
- Roles/Permissions
- Document Change Log
- Mobile SOS
- Mobile Carer
- CP Desktop
- CP Web
- Portal Web

## Ticket Knowledge

- SMAR tickets: `qa-knowledge/requirements/SMAR/`
- MA tickets: `qa-knowledge/requirements/MA/`

## Test Case Knowledge

- SMAR test cases: `qa-knowledge/test-cases/SMAR/`
- MA test cases: `qa-knowledge/test-cases/MA/`

## Regression Knowledge

- Regression map: `qa-knowledge/regression/regression-map.md`

## Decision Knowledge

- Confirmed BA/Dev/QA decisions: `qa-knowledge/decisions/decision-log.md`
