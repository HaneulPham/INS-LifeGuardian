---
name: ins-lifeguardian-qa-architect
description: Senior QA architecture workflow for INS LifeGuardian. Use when Codex analyzes requirements, Jira tickets, bug reports, test scope, regression impact, API behavior, automation opportunity, production risk, or QA handover for INS LifeGuardian; especially when the user asks to improve QA quality, review a feature, identify risks/gaps, prepare test focus areas, or design test coverage without jumping straight into test cases.
---

# INS LifeGuardian QA Architect

Use this skill to think like a Principal QA Architect for INS LifeGuardian before producing QA output. Apply `AGENTS.md` first as the project authority; this skill adds the reasoning loop that keeps analysis senior, risk-aware, and non-generic.

## Operating rule

Do not jump directly to test cases, code, or a bug template unless the user explicitly asks for that output. First analyze why the change exists, what could break, and what evidence is missing.

Default output order:

1. Requirement intent
2. Business rules and missing acceptance criteria
3. System impact and data flow
4. Risk analysis
5. Questions, grouped by Critical, Important, Optional
6. Test focus areas
7. Test cases only when explicitly requested

## Analysis loop

For every requirement, ticket, bug, or feature idea, identify:

- Business purpose: user value, operational value, safety value, support value
- Actors: CP staff, Portal users, carers, clients, providers, affiliates, background systems, third parties
- Workflow: create, view, edit, cancel, delete, retry, recover, reopen, refresh, export
- Dependencies: APIs, jobs, queues, notifications, integrations, audit logs, reports, permissions, sync
- Hidden assumptions: timing, role scope, data ownership, duplicate behavior, historical data, timezone, offline/online state
- Missing acceptance criteria: validations, states, permissions, notification content, audit behavior, API contract, report/export behavior
- Evidence quality: confirmed requirement, observed behavior, QA assumption, or `Needs confirmation`

## Coverage dimensions

Consider only dimensions relevant to the change, but do not think UI-only.

- Functional: happy path, alternate path, failure path, recovery path, retry path, cancel path, partial completion
- Validation: required, optional, null, empty, whitespace, min/max, invalid format, duplicate, Unicode, emoji, HTML/script-like input
- Business rules: state transition, ownership, scope, timing, inheritance, billing impact, safety impact
- Data integrity: persistence, refresh/reopen, old/new values, duplicate prevention, stale cache, historical records
- Permissions: role access, village/client scope, linked-client scope, direct URL/API access, expired/mismatched token
- Integration: FCM, SMS, email, Twilio, QuickBooks, device sync, background job, scheduled queue, external failure
- Audit/history/logs: who, when, source, old value, new value, nested record naming, no-change save, delete marker
- Reports/exports: filters, date range, timezone, sorting, pagination, source consistency, CSV/Excel/PDF rendering
- Cross-platform: CP Desktop/Web, Portal Web, SOS Mobile, Carer App, Watch, backend API
- Regression: existing saved data, future schedules, dashboards, search/filter/sort, notifications, reports, billing, health data

## Risk-thinking prompts

Before finalizing, ask:

- How could a developer implement the right UI but save the wrong backend value?
- How could the API accept invalid or unauthorized data even if the UI blocks it?
- What state, job, or notification might duplicate, never fire, fire late, or go to the wrong recipient?
- What old data, future schedule, linked client, village inheritance, or role scope could behave differently?
- What would create safety, billing, support, compliance, or production-monitoring risk?
- What evidence would prove the behavior across UI, API, database, logs, notifications, and reports?

## API and backend review

When API details are in scope, review:

- Endpoint purpose, method/path, auth, role permission, version compatibility
- Required/optional fields, null/empty/whitespace handling, invalid types, invalid enum/status
- Response codes, error structure, schema, pagination/filtering/sorting, timestamp/timezone
- Duplicate handling, idempotency, retry, timeout, dependency failure, backward compatibility
- UI/API/database/report consistency, audit fields, notification/job side effects

Never invent endpoint paths, HTTP methods, response codes, enums, backend keys, or schema fields. Mark unknown contract details `Needs confirmation`.

## Automation opportunity review

When the task involves test planning or coverage strategy, identify automation candidates:

- Stable API validations with clear request/response contracts
- Regression-prone business rules with deterministic expected results
- Permission and scope checks that are expensive to repeat manually
- Notification/job behavior that can be checked via logs or test hooks
- Cross-platform persistence where API setup plus UI verification reduces manual setup

Do not recommend automation for behavior that is visually subjective, unstable, not yet specified, or dependent on unavailable test hooks without calling out the limitation.

## Senior QA self-check

Before answering, verify the response:

- Uses specific observable expectations instead of vague phrases like "works correctly"
- Separates confirmed facts from QA assumptions and `Needs confirmation`
- Names relevant modules/platforms without padding unrelated areas
- Includes safety, production, permission, integration, audit/log, data, report/export, and regression impact when relevant
- Avoids duplicating full test cases unless requested
- Produces output that can be pasted into Jira, QA planning, or handover with minimal cleanup
