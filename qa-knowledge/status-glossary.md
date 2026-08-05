# INS LifeGuardian QA Knowledge Status Glossary

Use these statuses for all QA Second Brain knowledge.

| Status | Meaning | How Codex Should Use It |
|---|---|---|
| Confirmed | Requirement, BA/Dev/QA feedback, implemented behavior, or verified product behavior confirms this item. | Treat as reusable product knowledge. |
| QA Assumption | QA inferred this behavior from business logic or current workflow, but it is not explicitly confirmed. | Use carefully and mark as assumption in analysis/test cases. |
| Open Question | Behavior is missing, unclear, or needs BA/Dev confirmation. | Raise in Questions section before writing final test cases. |
| Out of Scope | Confirmed not included in this ticket or feature scope. | Do not write test cases unless regression impact exists. |
| Deprecated | Old behavior that should no longer be used. | Do not use for new test cases unless validating migration/backward compatibility. |
| Conflict | Existing knowledge conflicts with a new ticket, feedback, or implementation. | Report conflict before writing test cases. |

Do not treat **QA Assumption** or **Open Question** as **Confirmed**. Report **Conflict** before writing test cases or replacing confirmed knowledge.

Every requirement and module knowledge file must include a `Knowledge Status` table:

| Knowledge Item | Source Status | Source / Evidence | Last Updated | Notes |
|---|---|---|---|---|
| <item or section> | <supported status> | <ticket, decision, evidence, or observation> | <YYYY-MM-DD> | <context> |

## API Automation Statuses

These statuses apply only to `qa-knowledge/automation/api-automation-map.md` and the executable API mapping:

| Status | Meaning |
|---|---|
| Candidate | Approved manual API case appears suitable but is not implemented. |
| Automated | Implemented, validated, and mapped; last execution is recorded when available. |
| Partially Automated | Deterministic supported portion is automated; manual remainder is stated. |
| Blocked | Missing contract, access, data, environment, dependency, or instrumentation blocks implementation/execution. |
| Not Suitable | Safe deterministic API automation is inappropriate; reason is recorded. |
| Maintenance Required | Existing automation needs repair or contract-aligned update before reliable use. |

Automation status never changes the manual test case's approval or requirement status.
