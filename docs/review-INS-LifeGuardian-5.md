# INS LifeGuardian 5 — Codex QA Configuration Review

Date: 2026-07-22

## Review result

The repository has a strong progressive-disclosure architecture, evidence-first QA workflow, Analyst/Librarian separation, strict Second Brain gates, validators, unit tests, CI, and approved examples. The baseline automated suite passed before this update.

## Improvements added

1. Added a selectable question and confirmed-decision workflow with one decision per question, concrete options, `Other – specify`, safe recommendations, and case-impact updates.
2. Added an explicit override for users who request all groups or a complete suite, while keeping group-by-group review as the default.
3. Added **Requires Test Instrumentation** handling for internal behaviour that lacks observable evidence.
4. Added safe non-production test data, recipient isolation, cleanup/rollback, and audit-preservation rules.
5. Added privacy checks for notifications, logs, screenshots, reports, exports, errors, URLs, and tenant/client data.
6. Refined downstream non-trigger assertions so only realistically affected integrations are named.
7. Separated bug Severity from Priority and added explicit business/safety impact and evidence fields.
8. Added material-behaviour traceability to requirement intake and stored requirement templates.
9. Added behavior-contract tests and manual evals for the complete-suite override and instrumentation gap.

## Packaging finding

The supplied ZIP included `.git`, `.cache`, `.backups`, `.DS_Store`, `__MACOSX`, and pytest cache content. Share clean archives only. The delivered updated ZIP excludes those paths while preserving the current `.codex/config.toml` Confluence-read tool addition.

## Operational finding

The supplied repository had an uncommitted `.codex/config.toml` change. Because `require_clean_worktree: true`, automatic Second Brain updates would stop until that change is intentionally committed or otherwise resolved by the repository owner. The update is preserved in the clean deliverable; do not bypass the clean-worktree gate.
