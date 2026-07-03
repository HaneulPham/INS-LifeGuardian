# Decision: Start INS LifeGuardian QA Second Brain

Date: 2026-07-03

## Decision

Create a lightweight QA second-brain structure inside the INS LifeGuardian repository to preserve durable QA knowledge across tickets, screenshots, documents, bugs, risks, and regression planning.

## Why

INS LifeGuardian tickets often affect multiple surfaces, including CP Desktop, CP Web, Portal Web, SOS Mobile, Carer App, backend APIs, jobs/queues, notifications, audit/history/logs, reports/exports, and integrations.

A durable second brain helps preserve:

- Confirmed QA decisions
- Feature knowledge
- Repeated risk patterns
- Open questions
- Ticket analysis
- Regression maps
- Bug patterns
- Test design templates

## Guardrails

- `AGENTS.md` remains the always-read project instruction file.
- Second-brain notes are supporting QA memory only.
- Current Jira requirements, confirmed BA decisions, verified API contracts, and current product behavior take priority.
- Unknown or unverified details must be marked `Needs confirmation`.
- `AGENTS.md` changes still require user approval before editing.
