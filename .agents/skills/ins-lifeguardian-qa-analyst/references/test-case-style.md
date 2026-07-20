# Test-case design and style

Before writing cases, check the ticket index, related requirement and module files, existing cases, regression map, and decisions. Do not duplicate coverage solely for different wording, data, or navigation. Merge overlapping cases unless they verify a distinct rule, validation, role, platform, integration, failure mode, boundary, or regression risk; explain any overlap decision.

Write one requested group at a time. Use IDs `<Ticket>-G<Group>-<two-digit sequence>` such as `SMAR-2651-G1-01`. Allowed priorities are High, Medium, Low, and Lowest.

## Table schemas

UI/Mobile:

| TC ID | Priority | Test Area | Title | Preconditions | Test Steps | Expected Result | Expected Integration | Notes |
|---|---|---|---|---|---|---|---|---|

API:

| TC ID | Priority | API Endpoint | Method | Title | Preconditions | Request Data | Expected Response | Notes |
|---|---|---|---|---|---|---|---|---|

Regression:

| ID | Priority | Test Area | Summary | Preconditions | Test Steps | Check on CP | Check on Portal | Integration Check |
|---|---|---|---|---|---|---|---|---|

Steps must be numbered and reproducible. Give the first case in a group the full navigation flow; later cases may be shorter when Preconditions preserve an independently executable starting context.

Expected fields must be detailed, observable, and tied to existing step numbers using `**Verify after step #N:**`. Cover exact UI/API/database state and relevant integrations, including an explicit “no integration triggered” expectation when appropriate.

Group headings and `G<Group>` IDs must agree. Test Area must identify a module and feature rather than a broad platform label. Titles, summaries, expected fields, and responses must avoid vague wording. Number steps consecutively without gaps or duplicates; the first UI/Mobile case in a group must include the full navigation flow. API cases use GET, POST, PUT, PATCH, or DELETE and state an HTTP status; negative responses also describe the observable error or validation result. Normalize titles to identify potential duplicates.

After creating or updating stored cases, run both:

```bash
python3 scripts/validate_qa_test_cases.py
python3 scripts/validate_qa_knowledge.py
```

Do not treat cases as approved until validation passes.

## Good Expected Result Format

**Verify after step #4:**
- The dropdown opens successfully.
- Billing is displayed as a selectable Type.
- Billing appears exactly once.
- Billing is not disabled or visually unavailable.
- No blank, duplicate, or malformed Type value is displayed.

## Good Expected Integration Format

**Verify after step #7:**
- CP backend saves the selected Type value.
- Reopen API returns the saved value correctly.
- No duplicate record is created.
- No FCM, SMS, email, Twilio call, or alert escalation is triggered for this configuration-only update.

## Coverage selection

Choose relevant positive, negative, boundary, validation, recovery, permission, security, API consistency, integration, notification, jobs/queues, synchronization, persistence, data-integrity, audit/log, regression, compatibility, accessibility, performance, concurrency, idempotency, timezone, offline/network, report/export, and backward-compatibility categories. Do not force every category into every ticket.
