# INS LifeGuardian 4 — Codex QA Behaviour Review

Date: 2026-07-20

## Overall assessment

The uploaded project already had a strong architecture: root `AGENTS.md`, task-specific Analyst and Librarian skills, evidence-first requirement review, Second Brain status controls, strict Markdown validators, unit tests, and CI. The existing automated suite passed before modification.

The main weakness was not missing QA knowledge. It was insufficient behavioural demonstration and enforcement for the exact detailed-case style approved during live ticket work.

## Key gaps found

1. Detailed-case instructions were correct but too compressed; Codex had limited guidance on full workflow ordering, exact sample data, persistence checks, failure recovery, and no-false-export behaviour.
2. No approved full detailed-case example existed. The only approved example focused on requirement review, not test-case generation.
3. Reviewer/Rovo feedback had no formal Add/Update/Merge/Remove/Defer/Reject workflow.
4. The validator did not enforce the user preference that every UI/API title begins with `Verify ` and remains plain text.
5. The first-case navigation validator was weak: two steps and any navigation word could pass.
6. The validator allowed steps that depended on a previous test case.
7. There was no active approved-case ledger template to help preserve IDs and continue correctly with `next`.
8. There was no model-behaviour eval pack for scenarios static Markdown validation cannot assess.

## Improvements implemented

- Added an always-on Approved QA response behaviour section to `AGENTS.md`.
- Strengthened Analyst skill routing for detailed cases and reviewer feedback.
- Rebuilt the detailed test-case style reference with field-by-field production rules.
- Added a detailed test-case quality gate.
- Added a formal reviewer/Rovo feedback workflow.
- Added the SMAR-2633 approved detailed-case pattern as the primary golden example.
- Added write-group and reviewer-feedback prompt templates.
- Added an Approved Case Ledger and Deferred Scenarios to the test-case template.
- Strengthened the test-case validator to enforce:
  - UI/API titles begin with `Verify `;
  - titles are not fully bolded;
  - first UI case includes open/login, navigation, and record selection;
  - steps do not depend on another test case.
- Updated stored SMAR-2652 titles to comply with the approved style.
- Added behaviour-contract unit tests.
- Added manual Codex behaviour eval scenarios.
- Added `docs/codex-qa-behavior.md` explaining the architecture and usage.

## Verification completed

- Python compile: passed.
- Unit tests: 52 passed.
- Test-case validator: passed.
- QA knowledge validator: passed.

## Remaining limitation

No instruction set can guarantee identical wording on every model run. The combination of always-on instructions, progressive-disclosure skill references, a strong golden example, static validators, and manual behaviour evals provides substantially better consistency and makes drift visible.
