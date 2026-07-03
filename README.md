# INS LifeGuardian QA Workspace

This repository contains QA guidance and feature knowledge for INS LifeGuardian,
a healthcare, safety-monitoring, emergency-response, and client-support platform.

## How to use this repository

1. Read `AGENTS.md` before analyzing requirements or performing project work.
2. Complete requirement and risk analysis before creating test cases.
3. Generate test cases only when explicitly requested.
4. Mark unknown or unverified details as `Needs confirmation` rather than
   inventing requirements, API contracts, or system behavior.

## Feature context

- `WELFARE_CHECK_QA_CONTEXT.md` — Welfare Check requirements, behavior, risks,
  and supporting QA evidence.
- `SERVICE_REQUEST_QA_CONTEXT.md` — Service Request, Device Setup Checklist,
  cancellation, and Services Installed Summary knowledge.
- `DOCUMENT_FIELD_HISTORY_API_QA_CONTEXT.md` — Document Field History,
  Document Change Log, and SHM Client File API history knowledge.
- `NEW_SERVICE_REQUEST_STEPS_FOR_PERIPHERALS_QA_CONTEXT.md` — supporting QA
  context for new Service Request steps for peripherals.

Current Jira requirements and verified API contracts take precedence over the
supporting context files. Any conflicts must remain visible and be marked
`Needs confirmation` until resolved.

## QA second brain

- `second-brain/index.md` — entry point for durable QA memory.
- `second-brain/tickets/` — ticket-specific analysis notes.
- `second-brain/features/` — durable feature knowledge by module.
- `second-brain/decisions/` — confirmed QA/business working decisions.
- `second-brain/questions/` — open and resolved QA questions.
- `second-brain/risks/` — repeated risk and likely defect patterns.
- `second-brain/bugs/` — bug-writing guidance and recurring bug patterns.
- `second-brain/regression/` — regression maps and release coverage notes.
- `second-brain/templates/` — reusable ticket, bug, test design, and regression
  templates.

Second-brain notes are supporting QA memory only. Current Jira requirements,
confirmed BA decisions, verified API contracts, and current product behavior
take priority.

## Codex skills

- `.agents/skills/ins-lifeguardian-qa-architect/` — use for ordinary ticket,
  feature, screenshot, requirement, risk, regression, and QA coverage analysis.
- `.agents/skills/ins-lifeguardian-context-ingestion/` — use for larger source
  evidence ingestion from PDFs, Jira/Confluence exports, screenshots,
  spreadsheets, API collections, and historical test evidence.

## QA coverage

Analysis may include CP Desktop and Web, Portal Web, SOS Mobile, Carer App,
backend APIs, background jobs and queues, notifications, reports and exports,
audit/history/logs, integrations, permissions, cross-platform synchronization,
and data integrity.

## Repository safety

Do not commit credentials, access tokens, production client information, or
temporary document renders. Generated evidence under `tmp/` and operating-system
metadata such as `.DS_Store` are excluded from Git.
