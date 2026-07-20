# Automatic Requirement Intake

## Purpose

Automatically analyse supplied INS LifeGuardian requirement evidence and guide the user toward the next useful QA action. Use this mode when the user supplies a description, screenshot, Jira ticket, acceptance criteria, comment, file, API example, log, bug, reviewer feedback, or other feature evidence without a more specific command.

## Required Output

Use this structure, omitting only subsections that are genuinely irrelevant:

```markdown
# Requirement Intake — <Ticket ID or Feature Name>

## Evidence Received

- ...

### Could Not Verify

- ...

### Conflicting Evidence

- ...

### QA Assumptions

- ...

## Requirement Summary

...

## QA Analysis

### Business Workflow

...

### Validation and Data Rules

...

### Backend and Integration Impact

...

### Regression Impact

...

## Missing Requirements and Questions

### Critical

1. ...

### Important

1. ...

### Optional

1. ...

## Risks and Impact

| Risk | Impact | Area | Priority |
|---|---|---|---|

## Suggested Test Case Groups

| Group | Test Area | Coverage | Priority Focus |
|---|---|---|---|
| Group 1 | ... | ... | High |

## Suggested Next Prompts

- `Write detailed test cases for Group 1 only.`
```

### 1. Evidence Received

List the evidence reviewed, such as the ticket description, acceptance criteria, screenshots, Jira comments, API documentation, existing QA knowledge, and reviewer feedback. Always state **Could Not Verify** and **QA Assumptions**; add **Conflicting Evidence** when sources disagree. Do not present assumptions as confirmed behaviour.

For screenshots, record visible fields, labels, controls, values, states, navigation, validation, and errors as evidence. Treat persistence, integration, off-screen behaviour, and hidden or unreadable details as unverified unless another source confirms them.

### 2. Requirement Summary

Summarize the business intent, affected platform and module, actor, trigger, main behaviour, important validation, confirmed errors or messages, and expected stored or downstream result. Make the summary understandable without rereading the supplied evidence.

### 3. QA Analysis

Analyse only applicable areas:

- Positive, negative, retry, cancel, create, edit, delete, and reorder workflows
- Boundary values; required and optional fields; null, blank, whitespace, duplicate, and malformed values
- Roles, permissions, backend/API behaviour, persistence, and data integrity
- Jobs, queues, schedules, notifications, alerts, audit/history/logs, and reports
- External integrations and cross-platform synchronization
- Existing-data compatibility, upgrade, and migration impact
- Offline/network failures, concurrency, duplicate submissions, and idempotency
- Accessibility, production risk, and client-safety risk

Do not create artificial risks to fill the list or claim unverified root causes and downstream behaviour.

### 4. Missing Requirements and Questions

Group decision-ready questions as:

- **Critical**: Prevent reliable implementation, testing, security, or safety validation.
- **Important**: Affect expected behaviour, integration, regression, or coverage.
- **Optional**: Improve usability or completeness without blocking the main workflow.

Answer questions from available evidence rather than asking the user again.

### 5. Risks and Impact

Identify applicable business, client-safety, data-loss, duplicate-processing, notification/alarm, permission/privacy, integration, regression, backward-compatibility, and operational/support risks. State the affected platform or module and assign only justified priorities.

### 6. Suggested Test Case Groups

Propose logical groups without detailed test cases. For each group give its number, name, coverage objective, key scenarios, priority focus, and dependencies when applicable. Avoid overlap and scenarios duplicated only by wording, data, or navigation.

### 7. Suggested Next Prompts

End initial intake with a small, contextual set of copy-and-send prompts. Use only prompts relevant to the evidence.

Select from or adapt this command pool when applicable:

- `Deep analyse this requirement before test design.`
- `Review the missing requirements and propose expected behaviour.`
- `Compare this requirement with the QA Second Brain.`
- `Review backend, API, database, and integration impact.`
- `Review roles and permission impact.`
- `Review regression and cross-platform impact.`
- `Write detailed test cases for Group 1 only.`
- `Show sample data for the proposed test groups.`
- `Create an API test coverage matrix.`
- `Create a regression coverage matrix.`
- `Write a bug report from this evidence.`
- `Summarize the final approved requirement.`

For a new feature, prefer prompts such as:

- `Deep analyse the missing requirements before test design.`
- `Write detailed test cases for Group 1 only.`
- `Review backend, API, and database impact.`
- `Review regression and cross-platform impact.`

For a screenshot, prefer:

- `Analyse every visible field and interaction in this screenshot.`
- `Compare this screen with the ticket requirement.`
- `Propose validation and negative scenarios.`
- `Write detailed test cases for Group 1 only.`

For an API description, prefer:

- `Create the API test coverage matrix.`
- `Review authentication and permission scenarios.`
- `Review validation, persistence, duplicate, and idempotency behaviour.`
- `Review UI, API, and database consistency.`

For reviewer feedback, prefer:

- `Evaluate whether the reviewer feedback is valid.`
- `Identify which existing cases must be updated, merged, or removed.`
- `Show the proposed changes before rewriting the cases.`
- `Update Group 2 using the approved reviewer feedback.`

For a bug report, prefer:

- `Write a production-ready bug report.`
- `Analyse likely regression areas without claiming an unverified root cause.`
- `Propose focused reproduction and diagnostic checks.`
- `Identify related existing ticket coverage.`

When all cases are finished, prefer:

- `Summarize the final approved requirement.`
- `List all approved test groups and final case counts.`
- `Identify removed, merged, cancelled, and superseded cases.`
- `Approve and Update the QA Second Brain for ticket SMAR-XXXX`

Do not suggest the Second Brain approval command until the requirement and cases appear final or the user indicates approval.

## Default Restrictions

- Do not write all detailed test cases during intake.
- Do not save anything to the QA Second Brain without the exact approval command.
- Do not ask the user to repeat evidence already available in the conversation, Jira, attachments, screenshots, or QA knowledge.
- Do not claim a screenshot proves backend persistence or integration behaviour.
- Do not treat reviewer suggestions as approved requirements without confirmation.
