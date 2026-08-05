---
name: ins-lifeguardian-playwright-api-automation
description: Build, review, run, debug, fix, and map Playwright API automation for approved INS LifeGuardian API cases. API-only; never load browser/page-object rules.
---

# INS LifeGuardian Playwright API Automation

Use this skill only for Playwright API automation commands. It is intentionally separate from future Web automation.

## Supported commands

- `write API automation [for <case IDs>|ticket <ID>]`
- `review API automation [for <case IDs>|ticket <ID>]`
- `run API automation [for <case IDs>|ticket <ID>|tag <tag>|smoke|all]`
- `debug API automation failure [for <case ID>|result path]`
- `fix API automation [for <case IDs>|failure]`
- `update API automation mapping [for <case IDs>|ticket <ID>]`

Reuse active-ticket context and supplied evidence. Ask only for a missing item that makes safe implementation impossible.

## Hard boundary

This skill may create or modify only API automation, its documentation/configuration, and mapping. It must not create Web tests or:

- create Web tests, page objects, browser fixtures, locators, screenshots, or visual assertions;
- write or rewrite manual QA cases unless an automation blocker must be reported;
- update the QA Second Brain test-case source through the API mapping command;
- invent endpoint contracts or weaken approved expectations to make code pass.

## Evidence and entry gate

Use only:

1. approved Second Brain API test cases or explicitly supplied approved cases;
2. current Jira/Confluence/API contracts and confirmed decisions;
3. exact repository routes, schemas, handlers, auth rules, fixtures, and nearby tests;
4. verified non-production environment capability.

Every automated test must map to a manual case ID. Do not invent endpoints, methods, payload fields, status codes, error bodies, authorization rules, persistence effects, retries, or integration outcomes. Mark unsupported work **Could Not Automate**, **Requires Test Instrumentation**, or **Blocked** with the precise missing evidence.

## Progressive disclosure

Start with the requested case IDs and inspect only:

- `automation/api/README.md`, package/config files, mapping, and nearby automation;
- the exact approved cases, requirements, decisions, endpoint contract, implementation, and CI convention;
- one task-specific reference below when needed.

Load references selectively:

- implementation/review contract → `references/api-automation-contract.md`
- auth/tenant safety → `references/authentication-authorization.md`
- data and cleanup → `references/test-data-cleanup.md`
- assertions and evidence → `references/assertion-observability.md`
- failure triage → `references/failure-classification.md`
- mapping/status updates → `references/automation-mapping.md`

Do not load all references for every command.

## Command behavior

### Write

Inspect the current framework first. Use TypeScript and `@playwright/test` with standalone `APIRequestContext`. Reuse fixtures, clients, builders, helpers, and mapping conventions. Implement only requested approved cases; add exact traceability metadata; use safe unique data and deterministic cleanup; run static validation and the narrowest executable tests.

### Review

Review only requested/current automation. Check contract accuracy, traceability, isolation, auth/tenant boundaries, exact status/body/schema assertions, negative behavior, cleanup, secrets, retries, eventual consistency, duplication, and no browser dependencies. Return **Pass**, **Pass with Changes**, or **Blocked** plus exact changes.

### Run

Resolve the narrowest target and report the exact command, environment name, case IDs, passed/failed/flaky/skipped counts, report path, and blockers. Never claim execution when credentials, service access, or contracts are unavailable.

### Debug

Use the Playwright report, JSON result, request/response evidence, correlation IDs, logs, and approved behavior. Classify the failure before editing code. Never change an assertion merely because the product returned a different result.

### Fix

Change automation only when evidence shows an automation defect or maintainability issue. Preserve approved behavior and traceability. Re-run the failed test first, then the affected scope.

### Update mapping

After reviewed automation has an evidence-backed status, update both:

- `automation/api/mappings/automation-map.json`
- `qa-knowledge/automation/api-automation-map.md`

This command records automation state only. It does not change manual test-case approval or product requirements.

## Implementation rules

- Keep tests independent and parallel-safe.
- Use isolated non-production data; reject production execution.
- Keep credentials in environment variables and redact sensitive values.
- Use bounded evidence-backed polling for confirmed eventual consistency; never use arbitrary sleeps.
- Make cleanup idempotent and execute it after partial failure.
- Assert exact approved status, body/schema, headers, authorization, persistence-visible outcomes, and no-partial-save behavior.
- Keep one automated test aligned to one primary manual case goal unless the approved cases intentionally share one setup and outcome.
- Do not add dependencies or a second framework silently.
- Do not use `test.only`, committed `.env` files, production URLs, hard-coded tokens, or real client/health data.

## Validation

From `automation/api/`, run as applicable:

```bash
npm install
npm run validate
npm run test:case -- <case-id>
npm run test:ticket -- <ticket-id>
```

Run the narrowest target first. If live execution is unavailable, complete static validation and state exactly what was not executed.

## Completion output

Report:

1. Command and Scope
2. Automated or Reviewed Case IDs
3. Files Added or Updated
4. Validation and Execution Results
5. Mapping Changes
6. Deferred / Could Not Automate / Requires Test Instrumentation
7. Required Environment Variable names only
8. Cleanup and Data Safety
9. Remaining Concerns

Add at most one context-valid `Suggested next command:` line.
