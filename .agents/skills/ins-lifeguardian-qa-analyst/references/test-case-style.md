# Test-case design and style

Read this file together with `test-case-quality-gate.md` and the approved SMAR-2633 example before writing detailed cases.

Before writing cases, check the ticket index, related requirement and module files, existing cases, regression map, decisions, and the active conversation’s approved-case ledger. Do not duplicate coverage solely for different wording, sample data, or navigation. Merge overlapping cases unless they verify a distinct rule, validation, role, platform, integration, failure mode, boundary, recovery path, or regression risk.

Write one requested group at a time and stop for review by default. `next` means the next not-yet-reviewed group from the active plan. When the user explicitly requests all groups, a complete suite, or no review pauses, write all requested groups in order and apply the full quality gate to each. Preserve approved IDs. For additions, use the next unused two-digit sequence within the group; do not renumber approved cases unless the group structure changes.

Use IDs `<Ticket>-G<Group>-<two-digit sequence>` such as `SMAR-2651-G1-01`. Allowed priorities are High, Medium, Low, and Lowest.

## Table schemas

UI/Mobile/CP/Portal:

| TC ID | Priority | Test Area | Title | Preconditions | Test Steps | Expected Result | Expected Integration | Notes |
|---|---|---|---|---|---|---|---|---|

API:

| TC ID | Priority | API Endpoint | Method | Title | Preconditions | Request Data | Expected Response | Notes |
|---|---|---|---|---|---|---|---|---|

Regression:

| ID | Priority | Test Area | Summary | Preconditions | Test Steps | Check on CP | Check on Portal | Integration Check |
|---|---|---|---|---|---|---|---|---|

## Title rules

- Every UI and API Title begins with `Verify `.
- Keep the title as plain table text. Do not bold the entire title.
- State one specific, observable behaviour.
- Avoid vague titles such as `Verify feature works`, `Verify successful flow`, or `Verify validation`.
- Do not combine unrelated goals with `and`. Combining is acceptable only when the values are one atomic rule, such as preserving Rental Start Date while advancing Rental Start Period Date.

## Test Area rules

Use a concise module and feature, for example:

- `DVA Invoice Generation`
- `DVA Batch Validation`
- `Device Setup Steps — Delete Dependency`
- `Mobile Tasks — Check-in Sorting`

Do not use broad values such as `General`, `Testing`, `CP Web`, `Mobile`, or `Feature`.

## Preconditions rules

Include only scenario-specific setup:

- relevant status, role, client file, Work Order, invoice, device, asset, queue, integration stub, or feature configuration;
- exact test data needed to prove the rule;
- existing records that must or must not exist;
- values that must be recorded before the test;
- safe non-production recipients, stubs, queue state, or isolated test accounts when messages, alarms, calls, billing, or external integrations may trigger;
- cleanup or rollback needs for created records and downstream artefacts.

Do not repeat ordinary login, environment, or standard permissions unless they are part of the verification goal. Do not use real client health, contact, credential, or tenant data when synthetic or redacted data can prove the rule.

## Test Steps rules

Steps must be numbered, consecutive, action-based, and reproducible. Put no expected result inside a step.

The first case in each group must include the full execution path:

1. Open or log in to the applicable platform.
2. Navigate through the exact menu path.
3. Locate or select the prepared record or configuration.
4. Confirm the critical source data matches Preconditions.
5. Perform the action under test.
6. Open or review the generated/updated result.
7. Navigate to validation, export, log, report, mobile, or another downstream surface when applicable.
8. Inspect the final persisted or integrated output.

Use the actual workflow order. For example, generate an invoice from `Work Orders → Work Order Management` before navigating to `Raptor → DVA Submissions` for validation and export.

Later cases may be shorter, but must remain independently reproducible from their Preconditions. Do not write `continue from TC01`, `same as above`, or another dependency that prevents standalone execution.

Use one action per step where practical. Separate Save, refresh, reopen, validate, export, and inspect-output actions when each has an expected result.

## Expected Result rules

Group assertions by the exact step that produced the observable result:

`**Verify after step #N:**`

Use bullets and state exact observable outcomes, including applicable:

- displayed and saved values;
- enabled, disabled, editable, or read-only state;
- exact confirmed validation/error messages;
- record count and duplicate prevention;
- status transition or status preservation;
- sorting/order and persistence after refresh or reopen;
- blocked export, submission, deletion, or save;
- no partial save, no false success, and no stale value;
- unchanged values and behaviour that must remain unaffected.

Do not write `works correctly`, `successful`, `as expected`, `handled properly`, or multiple alternative outcomes. If the expected behaviour is unresolved, defer the scenario instead of writing `status remains Rejected or becomes Pending`.

## Expected Integration rules

Tie each integration assertion to a numbered step. Name only evidence-backed components and outcomes:

- backend API request/response;
- database persistence and atomicity;
- XML mapping and export records;
- queues/jobs, retries, and idempotency;
- FCM/push, SMS, email, Twilio;
- QuickBooks or billing integration;
- CP, Portal, Mobile, or Desktop synchronization;
- reports, notification logs, activity logs, audit/history, or Document Change Log.

For validation failures and configuration-only changes, explicitly state only the downstream processes that could realistically be reached by the tested action. Do not paste a broad non-trigger list into unrelated cases. Examples:

- no invoice record is created;
- no XML-generation job is queued;
- no FCM, SMS, email, or Twilio message is sent;
- no successful export/submission status is persisted;
- no duplicate queue message or audit entry is created.

Do not claim a database table, endpoint, queue, log, or integration is affected unless evidence establishes it. Use `where supported` only for optional observability, never for the primary expected behaviour.

If the primary rule cannot be observed through accessible UI, API, notification, report, export, audit/history, device activity, or approved test logs, do not disguise an internal assumption as an executable assertion. Add a **Requires Test Instrumentation** item naming the exact signal required, such as selected dialler number, queue payload and deduplication ID, cancelled-job status, FCM payload/topic, correlation ID, or export identifier.

For cases that trigger alarms, calls, SMS/email/push, invoices, exports, queue messages, device activity, or durable history, include a safe cleanup/rollback note. Verify cleanup removes only test artefacts, leaves unrelated data unchanged, and preserves audit evidence required for review. Verify client and contact information is not unnecessarily exposed in notifications, logs, screenshots, reports, exports, errors, or URLs.

## Notes and deferred scenarios

Use Notes for:

- confirmed source or acceptance-criteria mapping;
- a clearly labelled QA assumption;
- why a case is intentionally retained despite similarity;
- a dependency on a confirmed permission/status matrix.

Put unresolved business rules under a `Deferred Scenarios` section after the table. Do not create executable cases until the expected outcome is confirmed.

## Coverage selection

Choose only applicable positive, negative, boundary, validation, recovery, permission, security, API consistency, integration, notification, jobs/queues, synchronization, persistence, data integrity, audit/log, regression, compatibility, accessibility, performance, concurrency, idempotency, timezone, offline/network, report/export, and backward-compatibility coverage.

High priority is appropriate for core safety/business flows, validation, data integrity, alert/notification delivery, billing, export/submission, backend enforcement, or production risk. Medium covers important functional, permission, regression, and common boundary flows. Low and Lowest are for minor, uncommon, or cosmetic checks.

## Validation commands

After creating or updating stored cases, run:

```bash
python3 scripts/validate_qa_test_cases.py
python3 scripts/validate_qa_knowledge.py
```

Do not treat stored cases as approved until validation passes.
