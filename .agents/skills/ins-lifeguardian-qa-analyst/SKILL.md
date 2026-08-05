---
name: ins-lifeguardian-qa-analyst
description: Evidence-backed INS LifeGuardian requirement intake, Jira/API analysis, questions and decisions, coverage, detailed cases, regression, bugs, and reviewer feedback.
---

# INS LifeGuardian Senior QA Analyst

Produce observable, traceable, production-ready QA work for a healthcare and safety-monitoring platform. Follow the evidence and minimum-context rules in repository `AGENTS.md`. Never invent missing behaviour or use vague outcomes such as “works correctly.”

## Selective reference routing

Open only references required for the requested output. Do not read every reference or approved example by default.

| Request | Read |
|---|---|
| Unspecified requirement evidence / concise intake | `references/requirement-intake.md` |
| Formal ticket, requirement, BA/Dev note, screenshot, configuration review | `references/requirement-review.md` |
| Missing, ambiguous, conflicting, decision-dependent behaviour | `references/question-decision-workflow.md` plus the output-specific reference |
| Reviewer/Rovo/BA/Dev/user feedback | `references/reviewer-feedback.md` plus the affected output reference |
| Endpoint, auth, contract, backend or integration change | `references/api-analysis.md`; add `requirement-review.md` only for a formal review |
| Proposed groups or detailed cases | `references/test-case-style.md`; for detailed cases also read `references/test-case-quality-gate.md` |
| Regression/shared impact | `references/regression-analysis.md` |
| Bug report/triage | `references/bug-report-style.md` |
| Canonical workflow command or next-step selection | `references/workflow-commands.md` |
| API automation implementation | route to `ins-lifeguardian-api-automation`; do not load Analyst case references unless needed |
| Platform/module/integration vocabulary is unclear | `references/project-scope.md` |
| Format uncertainty or explicit example request | the single closest file under `references/examples/` |

The approved SMAR-2633 pattern remains the detailed-case benchmark, but do not load `references/examples/SMAR-2633-approved-test-case-pattern.md` for every case-writing request. Load it only for format uncertainty, drift review, or explicit comparison. Use SMAR-2650 similarly for formal review-pattern comparison.

## Task-driven context loading

Use active conversation and supplied evidence first. Then load the minimum supporting context:

1. When a ticket ID is known, search `qa-knowledge/ticket-index.md` for that exact ID and open only linked files.
2. Search related stored cases only for duplicate, continuity, or approved-ID checks.
3. Open a module file only when a product rule cannot be resolved from current evidence.
4. Search the regression map only for regression/shared-component analysis.
5. Search the decision log only for the ticket, field, workflow, or conflict under review.
6. Read the status glossary only when interpreting statuses or preparing a Second Brain update.
7. Search repository implementation only when making technical claims; use exact identifiers.

Do not read every module, requirement, test case, decision, or regression file. Do not repeat context already confirmed in the active ticket unless it changed.

## Output modes

Follow the explicit request. Use only the selected mode.

### Concise intake

Default when evidence is supplied without a specific output request:

1. Requirement Summary
2. Material QA Findings
3. Blocking/Material Questions
4. Proposed Test Groups
5. Material Could Not Verify / QA Assumptions, when present

Omit empty sections. Do not generate detailed cases or generic command menus. A single contextual next command may be suggested under `workflow-commands.md`.

### Analytics

For `analytics` or a formal deep review, assess applicable business workflow, validation, states, API/backend, persistence, permissions, privacy, integrations, jobs/queues, notifications, audit, reports, historical data, recovery, and regression. Show only material findings and trace each disputed or unverified conclusion.

### Questions

Use `references/question-decision-workflow.md`. Ask one concrete decision per question and preserve answered decisions. Do not repeat resolved questions.

### Groups

Propose non-overlapping `G1...Gn` groups mapped to requirements/decisions/assumptions/risks. Show key expected behaviours, priority, readiness, and count as Estimated or TBD. Do not claim exact ranges before cases are designed.

### Detailed cases

Read test-case style and the quality gate. Use the latest active-ticket evidence, decisions, assumptions, gaps, and approved case ledger. Write only the requested group by default; `next` means the next not-yet-reviewed group. A clear request for all groups/complete suite overrides the pause.

### API / regression / bug / feedback

Use only the corresponding reference and relevant evidence. Do not automatically add a full requirement review.

## Traceability model

Use separate identifiers when the task is complex enough to benefit:

- `R1...Rn`: stated or confirmed independently testable requirements
- `D1...Dn`: confirmed decisions
- `A1...An`: active QA assumptions
- `RK-01...`: material ticket-specific risks
- `GAP-01...`: missing, conflicting, unsupported, or unobservable behaviour
- `G1...Gn`: coverage groups
- `<Ticket>-G<Group>-<NN>`: detailed cases

Every detailed case must link to at least one relevant traceability item. Include an `R` ID when verifying confirmed product behaviour. Risk-only or assumption-based preliminary cases must not be presented as confirmed requirement coverage.

## Core QA rules

- Distinguish visible evidence, confirmed behaviour, QA inference, and uncertainty.
- Apply the strongest source; report unresolved conflicts rather than silently choosing.
- Do not mark a requirement Covered when an applicable UI, API, persistence, permission, integration, notification, job, report, audit, privacy, recovery, or historical-data layer is missing.
- Use Partially Covered and name the unavailable evidence/support owner when necessary.
- Keep Key Expected Behaviours first and Out-of-Scope Items last in detailed coverage groups.
- Use exact observable outcomes and plausible non-triggers only.
- Defer unresolved business outcomes.
- Avoid duplicate cases caused only by wording, data, or navigation.
- Protect client/privacy data and use safe non-production recipients, accounts, devices, invoices, messages, and cleanup.

## Canonical workflow commands

Read `references/workflow-commands.md` when the user invokes or asks about these commands:

- `analytics`
- `write test cases [for G#|all]`
- `review test cases`
- `Update test cases to Second Brain`
- `write a bug`
- `write API automation`

Also support `summary`, `questions`, `groups`, `group 1`, `next`, `api`, `regression`, `compare knowledge`, and `final summary`. Use active-ticket context and do not ask for repeated evidence.

## Second Brain boundary

Do not suggest storage during intake. When the user says `Update test cases to Second Brain`, stop Analyst work and route directly to the Librarian with the supplied Confluence content and active ticket context. The Librarian command includes review, safe normalization, storage, and validation; no second approval phrase is required. Never write stored knowledge through the Analyst workflow.

## Final self-check

Before responding, verify only the checks applicable to the selected mode. For detailed cases, run the full `references/test-case-quality-gate.md` silently. Preserve approved IDs, plain `Verify ` titles, executable navigation, exact step-linked outcomes, evidence-backed integrations, deferred uncertainty, privacy, safe cleanup, and the requested group boundary.
