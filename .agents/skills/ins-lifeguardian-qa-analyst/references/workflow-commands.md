# Canonical workflow commands

Treat these phrases as case-insensitive intent commands. Reuse the active ticket, decisions, group plan, and supplied evidence; do not ask the user to repeat available context.

## `analytics`

Perform any evidence-backed ticket QA analysis except detailed test-case rows or file writes. Cover only material requirements, gaps/conflicts, questions/decisions, assumptions, risks, groups, API/backend, permissions/privacy, integrations, jobs/queues, notifications, audit/history, reports, historical data, recovery, regression, feedback, bug impact, and automation suitability.

Do not update the Second Brain, modify automation, invent behaviour, or claim unsupported root cause. If groups are ready, suggest `write test cases for G1`.

## `write test cases [for G#|all]`

Generate executable cases from approved coverage:

- no target → next approved unwritten group;
- `for G2` → G2 only;
- `for all groups` → all approved groups in order.

Read the case style and quality gate. Preserve approved IDs and decisions. If no group is ready, update groups and stop. After writing, suggest `review test cases`.

## `review test cases`

Review only supplied/active cases against current evidence and the full quality gate. Classify Add, Update, Merge, Remove, Defer, Reject, or Retain. Check traceability, High/Medium/Low priority, IDs, duplication, executability, exact outcomes, integrations, evidence access, privacy, cleanup, and unresolved behaviour.

Return: Review Result (Pass / Pass with Changes / Blocked), Required Changes, Deferred or Could Not Verify, and Readiness. Suggest `next` when another group remains or `Update test cases to Second Brain` when the requested suite is ready.

## `Update test cases to Second Brain`

This is a direct execution command; do not require a second approval phrase. Route to `ins-lifeguardian-qa-librarian` with the supplied Confluence content and active ticket context.

The Librarian must retrieve the source; infer ticket/module/groups; apply the full case review; safely normalize IDs, priorities, `Verify ` titles, setup, steps, outcomes, integrations, traceability, counts, and formatting; preserve unique supported coverage; update only relevant requirement/case/decision/regression/module/index files; back up; validate; roll back on failure; and report all Add/Update/Merge/Remove/Retain/Renumber/Defer/Could Not Verify results.

Never invent behaviour. Preserve unsupported/conflicting items as Could Not Verify, Open Question, Conflict, or GAP while updating unrelated valid content. Ask only when the source/ticket cannot be identified or the whole write is unsafe. Do not suggest this command again after success.

## `write a bug`

Create one Jira-ready defect from observed evidence. Separate Actual Result, Expected Result, Severity, Priority, business/safety/privacy impact, evidence, and uncertainty. Do not generate cases or claim unsupported root cause.

## `write API automation`

Route to `ins-lifeguardian-api-automation`. Use approved or explicitly supplied API cases and current contracts only. Do not invent contracts or silently add dependencies/frameworks.

## Completion suggestions

After a substantive result, suggest at most one context-valid command:

`Suggested next command: <command>`

Do not show a menu, auto-run the suggestion, suggest a completed command, or suggest anything when no actionable next step exists.
