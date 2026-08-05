# INS LifeGuardian QA Second Brain Index

This folder is the durable supporting knowledge base for INS LifeGuardian QA.

Current Jira requirements, confirmed Jira comments, approved Confluence/API documentation, verified implementation evidence, and confirmed product behaviour take precedence over stored Second Brain knowledge.

When sources conflict, Codex must record the conflict and request clarification instead of silently selecting one behaviour.

## How Codex should use this knowledge

Use targeted retrieval; do not preload every file.

1. Start with supplied/current ticket evidence.
2. For a known ticket, open `ticket-index.md`, then only its linked requirement and test-case files.
3. Open `product-map.md` and one relevant module only when product context is needed.
4. Open the regression map only for shared-impact work.
5. Open the decision log only for prior decisions or conflicts.
6. Open the API automation map only for automation status work.

Do not invent missing product behavior. Record it as a requirement gap, QA assumption, or BA/Dev question as appropriate.

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

## Ticket Completion Gate

A ticket may be marked `Completed` in `ticket-index.md` only when:

- Its requirement file is not marked as migration pending.
- All approved test-case groups are stored as actual test-case rows.
- Strict test-case validation passes without `--allow-empty`.
- Neither the requirement nor test-case file contains a migration placeholder.
- The ticket index references existing requirement and test-case files.
- The requirement contains the standard `Knowledge Status` table.
- Confirmed decisions and regression impacts are recorded in their logs when applicable; use `None` in the corresponding requirement section when no log update applies.

`scripts/validate_qa_knowledge.py` enforces this gate for every ticket indexed as `Completed`; `scripts/validate_qa_test_cases.py` validates the stored case rows.

## Regression Knowledge

- Regression map: `qa-knowledge/regression/regression-map.md`

## Decision Knowledge

- Confirmed BA/Dev/QA decisions: `qa-knowledge/decisions/decision-log.md`

## API Automation Knowledge

- API automation map: `qa-knowledge/automation/api-automation-map.md`
- Executable framework: `automation/api/`
- API automation is separate from manual test-case approval and future Web automation.
