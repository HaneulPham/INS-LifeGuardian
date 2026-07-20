# API analysis

Apply this together with the requirement-review contract.

Review the endpoint purpose, route and method, authentication and role permissions, request/response schemas, required and optional fields, null/empty/whitespace values, invalid types, boundaries, invalid enums/statuses, duplicate requests, idempotency, retry behaviour, dependency failures, persistence, API/UI/database/report consistency, audit fields, compatibility, pagination, filters, sorting, and date/time handling.

Inspect API Gateway or routing configuration, authorizers, handlers, models/contracts, generated deployment output, automated tests, database mutations, downstream calls, and operational logs when available.

Do not assume an HTTP status, active consumer, authorization rule, or persistence outcome when the contract and implementation do not establish it.

For Postman or API coverage, propose groups for Positive, Negative, Validation, Auth/Security, Integration Failures, and Edge Cases, selecting only those that apply.
