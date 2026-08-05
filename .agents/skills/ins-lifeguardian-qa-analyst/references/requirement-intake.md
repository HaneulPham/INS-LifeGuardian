# Automatic Requirement Intake

Use when the user supplies INS LifeGuardian requirement evidence without requesting another specific output. The goal is a useful first review, not an exhaustive report.

## Default concise output

Omit empty sections.

```markdown
# Requirement Intake — <Ticket ID or Feature>

## Requirement Summary
- <confirmed or stated behaviour>

## Material QA Findings
- <important workflow, validation, data, API, integration, permission, privacy, job, notification, audit, historical-data, recovery, or regression finding>

## Blocking or Material Questions
Q1. <one concrete decision>
- A. <behaviour>
- B. <behaviour>
- C. Other – specify

## Proposed Test Groups
| Group | Coverage Area | Key Expected Behaviours | Priority | Readiness |
|---|---|---|---|---|

## Evidence Limitations and Assumptions
- **Could Not Verify:** ...
- **QA Assumption A1:** ...
- **Conflict:** ...
```

Do not include generic next-prompt lists. One context-aware `Suggested next command:` line is allowed when the next action is clear. Do not generate detailed test cases unless explicitly requested.

## Intake analysis rules

1. Separate stated/confirmed behaviour from QA inference.
2. Extract atomic requirements only when traceability materially helps; use `R1...Rn`.
3. Record the most precise source available: acceptance criterion, ticket paragraph, dated comment, screenshot, API section, decision, or verified repository evidence.
4. Use **Could Not Verify** only when missing evidence affects a conclusion or testability.
5. Name conflicting sources and behavioural differences; do not choose silently.
6. Ask only blocking or material questions. Use the question-decision workflow for multiple options and recommendations.
7. Propose non-overlapping groups; list exact expected behaviours rather than test-case titles.
8. Mark group readiness `Ready`, `Pending Decision`, or the specific blocker.
9. Use `Estimated` or `TBD`; do not invent exact case ranges before design.
10. Do not repeat background already established in the active ticket.

## Requirement Traceability

Use this only for multi-rule, disputed, safety-critical, integration-heavy, or formal reviews.

| Requirement ID | Material Behaviour | Source / Evidence | Status | Proposed Group |
|---|---|---|---|---|
| R1 | ... | ... | Stated / Confirmed / Pending Decision | G1 |

Keep separate identifiers for decisions (`D`), assumptions (`A`), risks (`RK`), gaps (`GAP`), and groups (`G`). Never place a QA assumption or risk inside an `R` requirement.

## Deep intake override

For `analytics`, “formal review,” or an explicit full analysis, expand only applicable areas:

- business workflow and state transitions;
- validation/data rules;
- API, persistence, auth, permission, tenant and privacy impact;
- integrations, jobs/queues, notifications, reports, audit/history;
- failure/retry/recovery, historical data, migration and compatibility;
- regression/shared-component impact;
- evidence reviewed, conflicts, assumptions, gaps and risks.

Do not create headings merely to say “none.”

## Screenshot and log evidence

For screenshots, distinguish visible fields, controls, values, states, navigation, and errors from off-screen inference. Record cropped, hidden, or unreadable details only when material.

For logs/errors, describe the observed failure and identifiers. Do not claim root cause without repository, runtime, API, database, or developer evidence.

## Restrictions

- No invented product, clinical, legal, privacy, security, permission, provider, or integration rules.
- No executable expected result for unresolved behaviour.
- No broad integration/non-trigger list unless the action can plausibly reach those components.
- No unnecessary personal, medical, contact, authentication, or tenant data.
- No full Second Brain scan; use targeted retrieval from `AGENTS.md` and the Analyst skill.
