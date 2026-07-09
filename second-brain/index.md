# INS LifeGuardian QA Second Brain Index

This is the entry point for durable INS LifeGuardian QA memory.

Use this second brain to preserve project learning from tickets, screenshots, documents, historical test evidence, QA decisions, bug patterns, risks, and regression knowledge.

Second-brain notes are supporting QA memory. Current Jira requirements, confirmed BA decisions, verified API contracts, and current product behavior take priority.

## How to use

Before analyzing a new ticket or document:

1. Read `AGENTS.md`.
2. Read this index.
3. Check any related feature, decision, risk, question, regression, or ticket note.
4. Keep confirmed facts, observed evidence, assumptions, conflicts, and open questions separate.
5. Mark unknown or unverified details as `Needs confirmation`.

## Main areas

| Area | Purpose |
| --- | --- |
| `raw/` | Notes about original evidence sources. Do not rewrite source meaning. |
| `tickets/` | One analysis note per Jira ticket or requirement. |
| `features/` | Durable feature knowledge by module. |
| `decisions/` | Confirmed QA/business decisions and working agreements. |
| `questions/` | Open questions, resolved answers, and confirmation history. |
| `risks/` | Repeated QA risks and likely defect patterns. |
| `bugs/` | Bug-writing knowledge and recurring bug patterns. |
| `regression/` | Regression maps and release-focused coverage notes. |
| `templates/` | Reusable analysis, bug, test design, and regression templates. |

## Existing project context files

These files still remain important feature knowledge sources:

- `../WELFARE_CHECK_QA_CONTEXT.md`
- `../SERVICE_REQUEST_QA_CONTEXT.md`
- `../DOCUMENT_FIELD_HISTORY_API_QA_CONTEXT.md`
- `../NEW_SERVICE_REQUEST_STEPS_FOR_PERIPHERALS_QA_CONTEXT.md`
- `../CARE_PLAN_TASKS_GENERAL_TASK_MOBILE_QA_CONTEXT.md`
- `../QA_COVERAGE_DIMENSIONS.md`
- `../INS_QA_ANALYSIS_FRAMEWORK.md`

## Starter feature map

| Feature / Module | Current knowledge source |
| --- | --- |
| Welfare Check | `../WELFARE_CHECK_QA_CONTEXT.md` |
| Service Request / Device Setup Checklist | `../SERVICE_REQUEST_QA_CONTEXT.md` |
| New Service Request Steps for Peripherals | `../NEW_SERVICE_REQUEST_STEPS_FOR_PERIPHERALS_QA_CONTEXT.md` |
| Document Field History / Document Change Log API | `../DOCUMENT_FIELD_HISTORY_API_QA_CONTEXT.md` |
| Care Plan Tasks - General Task Mobile | `../CARE_PLAN_TASKS_GENERAL_TASK_MOBILE_QA_CONTEXT.md`; `features/care-plan-tasks-general-task-mobile.md` |
| Billing | Needs dedicated feature note |
| Emergency Alarm | Needs dedicated feature note |
| Health Data / Charts | Needs dedicated feature note |
| Reports / Exports | Needs dedicated feature note |
| Portal Users / Permissions | Needs dedicated feature note |

## Key decisions

| Decision | Note |
| --- | --- |
| QA second brain started | `decisions/2026-07-03-qa-second-brain-start.md` |
| Skill routing for QA Architect vs Context Ingestion | `decisions/2026-07-03-skill-routing.md` |

## Working rule

Do not turn every note into test cases automatically. Use the second brain to improve analysis, find risk, preserve decisions, and design stronger QA coverage only when the user asks for test cases.
