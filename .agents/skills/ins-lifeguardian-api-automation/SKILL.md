---
name: ins-lifeguardian-api-automation
description: Implement evidence-backed API automation for approved INS LifeGuardian API test cases using the repository's existing framework and safe non-production data.
---

# INS LifeGuardian API Automation

Use this skill only for `write API automation`, equivalent explicit requests, or updates to existing API automation. Implement code in the current repository; do not perform general ticket analysis or write manual test-case matrices unless needed to resolve an automation blocker.

## Entry gate

Use only:

- approved API test cases from the active ticket;
- explicitly supplied automation scenarios;
- confirmed endpoint contracts, authentication rules, schemas, and expected responses;
- verified repository patterns.

Do not invent endpoints, methods, status codes, payload fields, authorization, database effects, or integration outcomes. Mark unsupported assertions **Could Not Automate** or **Requires Test Instrumentation**.

## Minimum-context discovery

Inspect only what is needed:

1. Existing API test framework, package/dependency files, test configuration, helpers, fixtures, and nearby tests.
2. Exact route, handler, contract/schema, auth, and persistence code for the selected cases.
3. Approved API cases and decisions for the active ticket.
4. CI command and environment-variable conventions.

Prefer the existing framework and style. When no framework exists: Do not add dependencies silently. Report the smallest viable framework choice and required decision unless the user explicitly asked to create a new framework.

## Automation selection

Automate scenarios that are deterministic, repeatable, safe, and observable through approved API responses or accessible evidence. Keep manual when they require unavailable providers, production-only behaviour, physical devices, human calls, inaccessible internal state, or unsafe personal/client data.

Map every automated test to its source case ID or traceability ID. Do not merge cases when distinct roles, auth states, payload boundaries, retries, integration states, or expected outcomes require separate setup/assertions.

## Implementation contract

- Reuse existing API clients, fixtures, builders, schemas, and assertion helpers.
- Keep secrets and tokens in approved environment variables; never commit credentials or production data.
- Use isolated non-production tenant/client/test records and deterministic unique identifiers.
- Add setup and cleanup that are idempotent and safe after partial failure.
- Assert exact evidence-backed status codes, response schema/body, headers, persistence-visible outcomes, authorization boundaries, and no-partial-save behaviour.
- Cover duplicate/idempotency, retry, negative auth, validation, and dependency failure only when supported by the approved cases and environment.
- Avoid brittle sleeps; use supported polling with bounded timeout when eventual consistency is confirmed.
- Redact personal, medical, contact, authentication, and tenant-sensitive values from logs and snapshots.
- Do not weaken existing assertions or unrelated tests to make the new automation pass.

## Execute and validate

Run the narrowest relevant test command first, then the broader affected suite when practical. Run formatting/lint/type checks required by the repository. If execution is blocked, report the exact missing dependency, variable, service, access, fixture, or contract; do not claim tests passed.

## Completion output

Report:

1. Automated Case IDs
2. Files Added or Updated
3. Test/Validation Commands and Results
4. Manual or Deferred Cases with reasons
5. Required Environment Variables by name only
6. Cleanup and test-data notes
7. Remaining concerns

When implementation and validation succeed, do not automatically update the QA Second Brain. Suggest a next command only when the active workflow clearly requires one.
