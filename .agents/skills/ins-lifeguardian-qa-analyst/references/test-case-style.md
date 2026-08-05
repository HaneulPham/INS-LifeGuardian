# Test-case design and style

Read with `test-case-quality-gate.md`. Load an approved example only when format uncertainty, drift review, or explicit comparison requires it.

Use the active ticket, latest decisions/assumptions, approved coverage plan, and only the existing cases needed for duplicate or ID continuity checks. Do not preload unrelated knowledge.

Write one requested group at a time and stop for review by default. When the user explicitly requests all groups, a complete suite, or no review pauses, write all requested groups in order. Preserve approved IDs; additions use the next unused two-digit sequence. Renumber only when group structure changes.

## IDs, traceability and priorities

- Case ID: `<Ticket>-G<Group>-<NN>`, for example `SMAR-2651-G1-01`.
- Add `Traceability IDs` when the ticket uses `R`, `D`, `A`, or `RK` identifiers.
- Include an `R` ID when verifying confirmed product behaviour.
- One case may cover multiple IDs only when setup, workflow, evidence, and final outcome align.
- Allowed priorities: High, Medium, Low.

## Schemas

UI/Mobile/CP/Portal:

| TC ID | Traceability IDs | Priority | Test Area | Title | Preconditions | Test Steps | Expected Result | Expected Integration | Notes |
|---|---|---|---|---|---|---|---|---|---|

API:

| TC ID | Traceability IDs | Priority | API Endpoint | Method | Title | Preconditions | Request Data | Expected Response | Notes |
|---|---|---|---|---|---|---|---|---|---|

Regression:

| ID | Traceability IDs | Priority | Test Area | Summary | Preconditions | Test Steps | Platform Checks | API / Integration Checks | Expected Outcome | Notes |
|---|---|---|---|---|---|---|---|---|---|---|

Use platform-neutral regression columns; do not force CP/Portal checks into mobile-, API-, job-, device-, or integration-only work.

## Title and Test Area

- Every UI/API Title is plain text beginning with `Verify `; do not bold the entire title.
- State one observable primary behaviour and condition.
- Avoid `works`, `successful flow`, `validation`, or unrelated goals joined with `and`.
- Test Area is a specific module/feature, not `General`, `Testing`, `CP Web`, `Mobile`, or `Feature`.

## Preconditions

Include only scenario-specific role, permission, tenant/client, record state, device/asset, integration/queue/job state, exact test data, existing/non-existing records, safe non-production recipients or stubs, and cleanup needs. Omit ordinary login/environment setup unless material.

Use synthetic/redacted data rather than real client health, contact, credential, authentication, or tenant data.

## Steps

- Number consecutively; one action per step where practical.
- Put no expected result in a step.
- The first case in a group includes the complete path: open/login, exact navigation, locate prepared record, confirm critical source data, perform the action, open/review the result, and inspect downstream output when applicable.
- Follow the actual workflow order.
- Later cases may be shorter but remain reproducible from Preconditions.
- Never use `continue from TC01`, `same as above`, or another cross-case dependency.
- Separate save, refresh/reopen, validate, export, retry, and downstream inspection when each creates a material result.

## Expected Result

Use bullets under `**Verify after step #N:**` when a particular step produces a material observable result. For simple navigation, group final outcomes under the final relevant step.

State applicable exact:

- displayed/saved values and labels;
- enabled, disabled, editable, read-only, selected, or sorted state;
- confirmed validation/error message;
- record count and duplicate prevention;
- status transition/preservation;
- persistence after refresh/reopen;
- blocked action, no partial save, no false success, and unchanged related data.

Do not use `works correctly`, `successful`, `as expected`, `handled properly`, or alternative unresolved outcomes. Defer unresolved behaviour.

## Expected Integration

Tie material integration assertions to a numbered step. Name only evidence-backed plausible components: API, persistence, export/XML, job/queue/retry, notification channel, billing/QuickBooks, cross-platform sync, report, notification/activity/audit history, or Document Change Log.

For failed or configuration-only actions, state only realistic non-triggers, such as no invoice, export job, notification, successful status, duplicate queue message, or audit event. Do not paste generic FCM/SMS/email/Twilio/billing/queue lists into unrelated cases.

Do not invent endpoints, tables, queues, logs, payloads, or root causes. `Where supported` is acceptable only for optional evidence, not the primary outcome.

When the primary rule is not observable through accessible UI, API, notification, report, export, audit/history, device activity, or approved logs, add **Requires Test Instrumentation** and name the exact signal needed.

For alarms, calls, SMS/email/push, invoices, exports, queue messages, device activity, or durable history, include a safe cleanup/rollback note. Cleanup must remove only test artefacts, preserve required audit evidence, and leave unrelated data unchanged.

## Notes, deferred scenarios and coverage

Use Notes for source mapping, a clearly labelled assumption, justified similarity, evidence access, or a confirmed matrix dependency. Put unresolved outcomes under `Deferred Scenarios`; do not create executable cases for them.

Select only risk-relevant positive, negative, boundary, validation, permission, security, recovery, integration, notification, job/queue, sync, persistence, audit, regression, compatibility, concurrency, idempotency, timezone, offline/network, report/export, privacy, and backward-compatibility coverage.

Merge duplicates caused only by wording, data, or navigation. Separate cases only for distinct rules, roles, platforms, boundaries, integration/failure states, evidence, final outcomes, or regression risks.

## Stored-case validation

After creating or updating stored cases, run:

```bash
python3 scripts/validate_qa_test_cases.py
python3 scripts/validate_qa_knowledge.py
python3 scripts/check_prompt_budget.py
```

Do not treat stored cases as approved until validation passes.
