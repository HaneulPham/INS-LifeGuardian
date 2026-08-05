# API automation contract

## Source and traceability

- Automate only approved API cases or explicitly approved scenarios.
- Test title format: `<CASE-ID> Verify <observable API behavior>`.
- Add `qa-test-case`, `requirement`, `endpoint`, and `method` annotations when supported.
- Add tags for ticket, group, module, API, priority, and optional smoke/regression scope.
- Keep the executable mapping and Second Brain mapping synchronized after validation.

## Test design

- One primary approved behavior per test.
- Tests are independent, parallel-safe, deterministic, and rerunnable.
- Use fixtures for request contexts and cleanup; clients for transport; builders for safe data; helpers for shared assertions.
- Avoid serial suites and cross-test state unless the approved workflow explicitly requires ordered lifecycle behavior and isolation is impossible.
- Use exact endpoint paths from evidence; do not centralize unconfirmed routes.

## Required checks when applicable

- method, path/query/header/body construction;
- expected status and content type;
- response schema and exact material values;
- authentication and authorization;
- tenant/client-file isolation;
- validation/error schema and no partial persistence;
- duplicate/idempotency behavior;
- persistence-visible GET or approved downstream evidence;
- bounded retry/polling only for confirmed eventual consistency;
- deterministic cleanup.

## Forbidden shortcuts

- arbitrary sleeps;
- catch-and-ignore failures;
- broad `expect.anything()` for material values;
- assertion deletion or status-code relaxation to make a failure pass;
- logging raw credentials, personal data, health data, or complete sensitive payloads;
- browser/page/locator use in the API project;
- unapproved production execution.
