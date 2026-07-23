# INS LifeGuardian Regression Map

This file stores reusable regression coverage and impact relationships across INS LifeGuardian modules, platforms, APIs, integrations, jobs, notifications, and reports.

## Usage Rules

- Add only reusable regression knowledge.
- Ticket-specific details should remain in the relevant requirement or test-case file.
- Mark unconfirmed behaviour as `QA Assumption` or `Open Question`.
- Update `Last Verified` when the regression relationship is confirmed again.

## Regression Coverage

| Module / Feature | Impacted Platforms | Core Regression Flows | Backend / API Impact | Integration Impact | Notifications / Jobs | Related Tickets | Source Status | Last Verified | Notes |
|---|---|---|---|---|---|---|---|---|---|
| Care Plan Tasks | CP Desktop, CP Web, Mobile SOS, Mobile Carer | Create, edit, delete, occurrence check-in, cross-platform refresh | Task and Task Occurrence APIs | CP/Mobile synchronization | FCM TaskUpdated, TaskDeleted, TaskDue, TaskReminder, TaskEscalation | MA-2136 | Confirmed | 2026-07-18 | Extend when additional task behaviour is approved |
| Service Requests | CP Desktop | Create, edit, process steps, device assignment; Device Setup add, delete, reorder, save, and false-persistence validation | Service Request backend APIs; independent SMAR-2652 API enforcement is an Open Question | Client File and device records | No notification should be triggered by setup-only changes unless configured | SMAR-2651, SMAR-2652 | Confirmed | 2026-07-20 | SMAR-2652 approved coverage confirms configuration-level dependency behavior; runtime processing is not included in its 11 approved cases |
| DVA Rental Invoices | CP Web | Invoice generation, date editing, boundary validation, IVL027, XML export, rejected resubmission, duplicate prevention, historical immutability, and Buy/Recycle regression | Persisted invoice rental dates; exact API routes and data objects are Open Questions | DVA XML HireStartDate and HirePrdStartDate mapping | Invalid invoices create no XML, export, queue, or DVA submission; no notification integration applies | SMAR-2633 | Confirmed | 2026-07-21 | Export uses persisted invoice values and does not recalculate from Work Order dates |
| Account Cancellation / Client File Suspension | Portal Web, Backend APIs | NoAuth login, existing billing/UI sequencing, direct suspension, suspension request, already-Suspended handling, targeting, failure handling, and duplicate prevention | `PATCH /lg/file/v2/{Uuid}` and `POST /lg/file/v2/{Uuid}/statusrequest`; exact status/error contracts remain Open Questions | Portal → AWS NoAuth; AWS → old backend through `InsService` and SMAR-2657 HMAC | Direct suspension creates a 30-day deletion lifecycle; status request uses the configured enquiries workflow; exact jobs and queues are Open Questions | SMAR-2635, SMAR-2657 | Confirmed | 2026-07-23 | Portal must not call the old dispatcher directly or retain the deprecated Portal HMAC credentials for these actions |

## Cross-Module Regression Relationships

| Changed Area | Related Areas to Recheck | Reason | Source Status | Related Tickets |
|---|---|---|---|---|
| Task schedule or reminder configuration | Mobile Task List, FCM, Carer activity, SMS, email, alarm escalation | Schedule changes may affect task timing and downstream notifications | Confirmed | MA-2136 |
| Device Setup Steps | Service Request Process, Client File devices, CAMS/INS asset creation | Setup templates determine the runtime service-request workflow | Confirmed | SMAR-2652 |
| Service Request Type | Service Request create/edit, filtering, reports, permissions | Type changes may affect available workflow and reporting | QA Assumption | SMAR-2651 |
| DVA rental invoice date generation or editing | IVL027 validation, DVA XML export, rejected resubmission, historical invoices, duplicate export protection, Buy and Recycle invoices | Persisted invoice dates drive validation and export while non-rental purchase types must remain unaffected | Confirmed | SMAR-2633 |
| Portal Account Cancellation request routing or authentication | No-billing, IAB, Village/LinkingCode, other-active-service, already-Suspended, deletion scheduling, enquiries workflow, and Portal deployment | The same user action selects a destructive direct-suspension route or a non-destructive suspension-request route, while removal of Portal HMAC credentials must not change existing UI/billing sequencing | Confirmed | SMAR-2635, SMAR-2657 |
