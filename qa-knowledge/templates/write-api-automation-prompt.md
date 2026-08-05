# Write API Automation Command

```text
write API automation

Automate the approved API test cases for the active INS LifeGuardian ticket using the repository's existing automation framework and patterns.
Inspect only the exact cases, contracts, routes, auth, helpers, fixtures, nearby tests, and CI configuration required.

Map automation to source case IDs. Use safe non-production data, environment variables for secrets, deterministic setup/cleanup, and exact evidence-backed assertions. Run the narrow affected tests and required lint/type checks.

Do not invent endpoints or expected responses, add a new framework silently, automate unsafe or unobservable scenarios, or claim execution passed when blocked.
Report automated IDs, files changed, commands/results, deferred manual cases, required environment-variable names, cleanup, and remaining concerns.
```
