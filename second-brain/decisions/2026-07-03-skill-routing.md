# Decision: INS LifeGuardian Skill Routing

Date: 2026-07-03

## Decision

Use the existing `ins-lifeguardian-qa-architect` skill for ordinary ticket, feature, screenshot, requirement, risk, regression, and QA coverage analysis.

Use the `ins-lifeguardian-context-ingestion` skill for larger evidence ingestion, such as PDFs, Jira/Confluence exports, screenshots, spreadsheets, API collections, historical test cases, and other artifacts that should become durable feature context or second-brain knowledge.

## Why

The project already has a QA Architect skill that covers the intended ticket-analysis workflow. Updating that skill avoids creating a duplicate `ticket-analysis` skill with overlapping behavior.

## Guardrails

- Read `AGENTS.md` first.
- Read `second-brain/index.md` when durable QA memory is relevant.
- Treat second-brain notes as supporting memory, not the final source of truth.
- Do not write test cases unless the user explicitly asks.
- Keep unknowns marked as `Needs confirmation`.
- For Client File screenshots that need Document Field History mapping, apply the
  `Screenshot-to-history mapping workflow` in `AGENTS.md`: separate editable
  fields, read-only/status fields, and action buttons; keep the requested
  numbering; use old/new value rules for tracked fields; and avoid treating
  action buttons as audited document fields unless confirmed.
