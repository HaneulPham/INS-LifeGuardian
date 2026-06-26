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

Current Jira requirements and verified API contracts take precedence over the
supporting context files. Any conflicts must remain visible and be marked
`Needs confirmation` until resolved.

## QA coverage

Analysis may include CP Desktop and Web, Portal Web, SOS Mobile, Carer App,
backend APIs, background jobs and queues, notifications, reports and exports,
audit/history/logs, integrations, permissions, cross-platform synchronization,
and data integrity.

## Repository safety

Do not commit credentials, access tokens, production client information, or
temporary document renders. Generated evidence under `tmp/` and operating-system
metadata such as `.DS_Store` are excluded from Git.
