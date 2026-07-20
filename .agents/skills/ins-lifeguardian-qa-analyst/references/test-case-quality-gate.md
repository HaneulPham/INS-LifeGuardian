# Detailed test-case quality gate

Run this self-review before returning a test-case group. Correct failures before responding.

## Scope and continuity

- Only the requested group is included.
- The group matches the active approved coverage plan.
- `next` selected the next not-yet-reviewed group.
- Existing approved IDs and content are preserved unless feedback explicitly changes them.
- New IDs use the next unused two-digit sequence.

## Coverage quality

- Every case has one primary verification goal.
- No case duplicates another solely through different data or wording.
- Positive, negative, boundary, recovery, permission, integration, or regression cases are included only when they prove distinct risk.
- Unconfirmed behaviour is deferred rather than invented.
- Out-of-scope behaviour is not tested except for justified regression protection.

## Executability

- The first case has full platform and menu navigation.
- The tester can identify and prepare all records from Preconditions.
- Critical source values are confirmed before the action.
- Steps follow the real workflow order.
- Save, refresh/reopen, validate, export, and downstream inspection are separate when needed.
- No step contains an expected result.
- Later cases remain reproducible without relying on an earlier case.

## Title and metadata

- UI/API Title starts with `Verify `.
- Title is not fully bolded.
- Test Area is specific.
- Priority is one of High, Medium, Low, Lowest and matches business/safety risk.
- Preconditions contain only scenario-specific setup and exact data.

## Expected Result

- Every assertion is grouped under `**Verify after step #N:**` and references a real step.
- Exact values, messages, status, editability, blocked actions, and persistence are stated where applicable.
- Refresh/reopen verifies saved data for create/update/delete.
- Failure cases verify no partial save, no false status, and recovery availability.
- Unchanged fields and related workflows are protected where regression risk exists.

## Expected Integration

- Assertions identify the backend/API/database/export/job/log behaviour that can be observed.
- Duplicate requests, retries, queues, and idempotency are covered when relevant.
- Failed or configuration-only actions explicitly state which integrations do not trigger.
- Cross-platform consistency is included only when the feature has another consumer.
- No unverified root cause, endpoint, database table, or integration is invented.

## Output finish

- Deferred questions are listed separately.
- The response stops after the requested group and waits for review.
- The group can be pasted into Jira, Confluence, or the Second Brain without restructuring.
