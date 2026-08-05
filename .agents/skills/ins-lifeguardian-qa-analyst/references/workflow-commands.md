# Canonical workflow commands

Treat commands case-insensitively. Reuse active-ticket context; reuse supplied evidence.

## `analytics`

Perform any evidence-backed ticket QA work except detailed case rows, automation edits, or file writes. Cover only material requirements, gaps/conflicts, questions/decisions, assumptions, risks, groups, API/backend, privacy/permissions, integrations, jobs/queues, notifications, audit/history, reports, recovery, regression, bug impact, and automation suitability. Do not invent behaviour or root cause. Suggest `write test cases for G1` only when groups are ready.

## `write test cases [for G#|all]`

Use approved coverage:

- no target → next approved unwritten group;
- `for G2` → G2 only;
- `for all groups` → every approved group in order.

Apply case style and quality gates, preserve approved IDs/decisions, and stop if no group is ready. Suggest `review test cases` after writing.

## `review test cases`

Review supplied/active cases against evidence and the full quality gate. Classify Add, Update, Merge, Remove, Defer, Reject, or Retain. Check traceability, High/Medium/Low priority, IDs, duplication, executability, outcomes, integrations, evidence access, privacy, cleanup, and unresolved behaviour.

Return Pass, Pass with Changes, or Blocked; list required changes, deferred/Could Not Verify items, and readiness. Suggest `next` or `Update test cases to Second Brain` only when appropriate.

## `Update test cases to Second Brain`

This is a direct execution command; do not require a second approval phrase. Route supplied Confluence content and active context to `ins-lifeguardian-qa-librarian`.

Retrieve and review the source; infer ticket/module/groups; normalize supported IDs, priorities, `Verify ` titles, setup, steps, outcomes, integrations, traceability, counts, and formatting; preserve unique coverage; update only relevant requirement/case/decision/regression/module/index files; back up, validate, and roll back on failure. Report Add/Update/Merge/Remove/Retain/Renumber/Defer/Could Not Verify.

Never invent behaviour. Preserve unsupported/conflicting items as Could Not Verify, Open Question, Conflict, or GAP while updating unrelated valid content. Ask only when identification or the whole write is unsafe. Do not suggest this command again after success.

## `write a bug`

Create one Jira-ready defect from observed evidence. Separate Actual Result, Expected Result, Severity, Priority, business/safety/privacy impact, evidence, and uncertainty. Do not generate cases or claim unsupported root cause.

## Playwright API automation commands

Route these to `ins-lifeguardian-playwright-api-automation`; keep API and future Web automation separate.

- `write API automation [for <IDs>|ticket <ID>]` — implement approved requested API cases.
- `review API automation [for <scope>]` — apply the automation quality gate without changing product behaviour.
- `run API automation [for <scope>|smoke|regression|all]` — run the narrowest non-production target.
- `debug API automation failure [for <case/result>]` — classify from approved behaviour and execution evidence before editing.
- `fix API automation [for <scope>]` — fix proven automation defects and rerun narrow scope.
- `update API automation mapping [for <scope>]` — synchronize executable and Second Brain status after evidence.

Do not create browser tests, invent contracts, add another framework silently, use production data, or claim unexecuted tests passed.

## Completion suggestions

After a substantive result, add at most one context-valid line: `Suggested next command: <command>`. Do not show a menu, auto-run it, repeat a completed command, or suggest a step with no actionable purpose.
