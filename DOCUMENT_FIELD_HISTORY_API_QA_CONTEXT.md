# INS LifeGuardian Document Field History API QA Context

Use this document as supporting QA evidence when analyzing Document Field History, Document Change Log, or SHM Client File API create/update behavior. Current Jira requirements and verified API contracts take precedence. Conflicts and incomplete contract details are marked `Needs confirmation`.

## Purpose and authority

This context captures the intended correction in SMAR-2334 and the supplied DocumentFieldHistory API definition. It does not prove that the change is deployed or describe the complete SHM Client File API contract.

## Source documents

- SMAR-2334: Document Field History Platform Incorrect for SHM Client File API's, supplied as a ticket screenshot.
- `BA-DocumentFieldHistory API.pdf`, a Confluence export describing LG Document Field History v2 properties and operations.
- Repository `AGENTS.md`, including confirmed Document Change Log formatting rules.
- Sources reviewed on 23/06/2026.

## Evidence interpretation

- SMAR-2334 expected results are treated as confirmed requirements for the ticket scope.
- SMAR-2334 actual results are observed defect behavior for the SHM API old backend, not desired behavior.
- The PDF is treated as the supplied API definition for `/lg/documentfieldhistory/v2`; current deployed schemas and behavior still require verification.
- The PDF's example tenant, UUIDs, people, and source names are execution-specific and must not be reused in test data.
- The SHM `CreateClientFileRequest` and `UpdateClientFileRequest` endpoints, methods, response codes, and full schemas were not supplied and must not be guessed.

## Feature purpose

Document Field History provides an auditable record of client-file and other source changes. SMAR-2334 corrects attribution and completeness when client files are created or updated through the SHM API so CP users do not see API-originated changes incorrectly attributed to Control Panel and do not receive incomplete or unreadable history.

The business value is reliable traceability: users reviewing Document Change Log must be able to identify the originating platform and understand which client-file values were created or changed.

## Platforms and components

- SHM API old backend: produces Client File create/update operations and their history records.
- IPD: identified by SMAR-2334 as the default originating platform when SHM requests do not set `EditedBy`.
- LG Document Field History API v2: stores and retrieves field-history records.
- CP Document Change Log: displays the resulting history for the client file.
- Mobile/Postman are cited as request origins in the defect reproduction, but their exact platform-to-enum mapping is `Needs confirmation`.
- Portal behavior is outside the explicit ticket scope; regression impact is `Needs confirmation` if it consumes the same history records.

## Roles and permissions

- The supplied sources do not define which roles may call the SHM Client File endpoints, create history directly, or view Document Change Log. `Needs confirmation`.
- QA must verify that history retrieval and CP display remain scoped to the authorized tenant and client file, with no cross-client or cross-tenant leakage.
- Authentication, direct-API authorization, expired token behavior, and read-only versus edit permissions are `Needs confirmation` for the supplied endpoints.

## Terminology and data model

### SHM request attribution

- `EditedBy` must be added to `CreateClientFileRequest`.
- `EditedBy` on both `CreateClientFileRequest` and `UpdateClientFileRequest` must be nullable and use type `DocumentHistoryPlatform`.
- When `EditedBy` is omitted, blank, or null, the effective history platform must default to `IPD`.
- Before the fix, absent attribution was observed as `ControlPanel`, which SMAR-2334 identifies as incorrect.
- Supported non-null `DocumentHistoryPlatform` values and serialization rules are `Needs confirmation`.

### Document Field History properties

The supplied v2 API definition lists these properties:

- `Ten` (`String`): tenant.
- `SrcUuid` (`Guid`): source identifier.
- `SrcName` (`String`): source name.
- `SrcType` (`Documenthistorysource`): source type.
- `SrcPfm` (`Userplatform`): source platform.
- `SrcFld` (`String`): source field.
- `SrcFldUuid` (`Guid`): nested/source-field identifier where applicable.
- `SrcFldName` (`String`): source-field name.
- `OldSrcFldName` (`String`): previous source-field name.
- `Val` (`String`): new value.
- `OldVal` (`String`): old value.
- `UpdAt` (`Long`): server-set update time as epoch milliseconds.
- `UpdUuid` (`Guid`): updater identifier based on its type and sample shape; the PDF description is inconsistent and requires confirmation.
- `UpdBy` (`String`): updater display/reference text based on its type and sample shape; the PDF description is inconsistent and requires confirmation.

The precise mapping from SHM `EditedBy` to history `SrcPfm` is strongly implied by SMAR-2334 but not explicitly documented in the supplied API definition. Confirm the implementation mapping while testing.

## Workflows and state transitions

### Create client file through SHM API

1. Submit a valid `CreateClientFileRequest`.
2. The SHM backend creates the client file and generates Document Field History records.
3. If `EditedBy` is absent, blank, or null, generated history uses platform `IPD`, not `ControlPanel`.
4. All applicable Client and Client File fields supplied during creation are logged.
5. Medication is logged as a readable formatted value containing Name, Dosage, and Comment.
6. CP Document Change Log displays the generated records for the new client file.

### Update client file through SHM API

1. Submit a valid `UpdateClientFileRequest` for an existing client file.
2. If `EditedBy` is absent, blank, or null, generated history uses platform `IPD`, not `ControlPanel`.
3. Changed fields generate the applicable history records and CP displays them after refresh/reopen.

Exact no-change, clear/remove, nested-record update, and invalid-request behavior on the SHM endpoints is not specified by SMAR-2334; apply current verified Document Change Log rules and mark contract gaps `Needs confirmation`.

## UI behavior

- CP Document Change Log is the stated verification surface for create and update results.
- The displayed Platform must represent the effective source platform. For an omitted, blank, or null `EditedBy` in these SHM requests, it must display `IPD` rather than `ControlPanel`.
- Create history must include both Client and Client File fields that are applicable to the submitted request.
- Medication must render as readable business text containing Name, Dosage, and Comment; raw JSON, object text, or an incomplete value is not acceptable.
- Exact CP labels for every Client File field and the complete create-field inventory are `Needs confirmation`.

## Backend and API behavior

### SHM Client File requests

- `CreateClientFileRequest.EditedBy`: nullable `DocumentHistoryPlatform`; defaults effectively to `IPD` when omitted, blank, or null.
- `UpdateClientFileRequest.EditedBy`: nullable `DocumentHistoryPlatform`; defaults effectively to `IPD` when omitted, blank, or null.
- Create must generate history for all applicable Client File fields, not only Client fields.
- Create must generate Medication history in the confirmed readable Name, Dosage, and Comment format.
- Exact endpoint URLs, HTTP methods, response codes, request field inventory, null-versus-empty-string deserialization, invalid enum errors, and transaction behavior are `Needs confirmation`.

### LG Document Field History v2 retrieval

- `GET {{domain}}/lg/documentfieldhistory/v2?SrcUuid={{SrcUuid}}&PageSize={{PageSize}}&SrcField={{SrcField}}` retrieves paginated history by source and optionally by field. The PDF also lists `PageToken` as optional.
- `GET {{domain}}/lg/documentfieldhistory/v2?UserUuid={{UserUuid}}&PageSize={{PageSize}}` retrieves paginated history by user. The PDF also lists `PageToken` as optional.
- A successful retrieval returns `200 OK` with `Result` history objects and `PageToken` according to the sample.
- The PDF documents `400 Bad Request`, `404 Not Found`, and `500 Internal Server Error` outcomes but does not define exact error bodies.
- Behavior when source and user filters are combined, when all filters are absent, and for invalid pagination values is `Needs confirmation`.

### LG Document Field History v2 field discovery

- `GET {{domain}}/lg/documentfieldhistory/v2/fields?SrcUuid={{SrcUuid}}` returns available source fields.
- The PDF shows `200 OK`, `400 Bad Request`, `404 Not Found`, and `500 Internal Server Error` outcomes.
- The PDF example omits `SrcUuid` despite listing it as a query parameter. Whether it is required is `Needs confirmation`.
- The response description says "paged" while the sample is a plain string array. Pagination behavior is `Needs confirmation`.

### LG Document Field History v2 creation

- `POST {{domain}}/lg/documentfieldhistory/v2` accepts an array of Document Field History records.
- The documented successful response is `200 OK` with an empty body.
- The PDF documents `400 Bad Request` for validation failure or an already-existing Activity Stream and `500 Internal Server Error` for server failure.
- The reference to "Activity Stream" appears inconsistent with Document Field History and is `Needs confirmation`.
- Required fields, server-controlled fields, duplicate identity, idempotency, partial-batch handling, and authorization are not defined.

## Reports, exports, audit, and history

- Document Field History and CP Document Change Log are the audit/history outputs in scope.
- For create operations, the repository rule is Old Value blank and New Value populated.
- For update operations, Old Value is the previous readable value and New Value is the updated readable value.
- Clear/remove/delete uses New Value `~DELETED~` where the current Document Change Log rules apply.
- Medication is nested data and must use a meaningful source/subfield association only where applicable.
- The same logical field change must not create duplicate history records.
- Report/export consumers of Document Field History are not identified in the supplied sources. `Needs confirmation`.

## Data integrity and security

- Client-file persistence and generated history must agree: no missing field record, wrong source/client association, unrelated field update, or duplicate record.
- A history-generation failure must not silently leave an untraceable client-file mutation. Whether the business transaction rolls back or records/retries the audit failure is `Needs confirmation`.
- Tenant, client-file, updater, and platform attribution must not be taken from untrusted values without the backend authorization and validation defined by the current contract.
- The `EditedBy` default must remain backward compatible for IPD callers that do not send the new property.
- Explicit platform spoofing rules and whether callers may set `ControlPanel`, `Portal`, or other values are `Needs confirmation`.

## Confirmed validation themes

- Create with `EditedBy` omitted, explicit null, and any request representation treated as blank by the API defaults history Platform to `IPD`.
- Update with the same attribution variants defaults history Platform to `IPD`.
- Explicit supported non-null platform values persist accurately once the allowed enum set is confirmed.
- Create logs every applicable Client and Client File field with correct source field, source name, new value, and no unrelated or duplicate records.
- Medication create history contains readable Name, Dosage, and Comment values and does not expose raw JSON or object serialization.
- History is retrievable through v2 by the created/updated source and appears consistently in CP after refresh/reopen.
- Existing callers that omit `EditedBy` continue to create or update client files while receiving the corrected `IPD` attribution.
- Permission, token, tenant, client-file scope, invalid enum, null/empty handling, duplicate request, retry, and concurrent update behavior require contract-led coverage.

## Open questions and source conflicts

### Critical

- What are the exact SHM Create Client File and Update Client File endpoint URLs, HTTP methods, authentication rules, success/error codes, and request/response schemas?
- Does omitted, JSON `null`, and empty-string `EditedBy` all deserialize to the same default path? The ticket groups blank/null but does not define wire-level validation.
- What is the complete list and exact mapping of Client File fields that must be logged by `CreateClientFileRequest`?
- Does `EditedBy` map directly to history `SrcPfm`, and which `DocumentHistoryPlatform` values are allowed for SHM callers?
- If client-file persistence succeeds but history creation fails, must the transaction roll back, retry, queue recovery work, or raise an operational alert?

### Important

- What exact separator, labels, blank-component handling, and order define the readable Medication format beyond Name, Dosage, and Comment?
- Are explicit but unauthorized or semantically incorrect platform values rejected, ignored, or accepted?
- Are the PDF descriptions for `UpdUuid` and `UpdBy` reversed? Their declared types and samples suggest UUID versus display name respectively.
- Is `SrcUuid` required for `/fields`, and is that response paginated or a plain string array?
- What makes a POSTed history record a duplicate, and is batch creation atomic?

### Optional

- Do reports or exports consume these same records and require regression validation?
- Does Portal display SHM-created Client File history, and if so, which Platform label must it show?
- Should historical records incorrectly stored as `ControlPanel` be migrated, or does the fix apply only to newly created history?

## Required QA posture

- Treat this as audit-integrity and attribution work, not merely a nullable-field change.
- Validate the SHM mutation, stored/retrieved history, and CP presentation as one chain.
- Compare the exact submitted fields with generated records, including old/new values, source/subfield identity for nested data, updater, timestamp, tenant, client file, and platform.
- Use neutral test data and never copy identifiers or people from the API document samples.
- Do not write literal SHM API test cases until its endpoint contract is supplied or verified; mark missing contract values `Needs confirmation`.
- Preserve the distinction between SMAR-2334 observed failures and the required post-fix behavior.
