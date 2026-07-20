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

## Cross-Module Regression Relationships

| Changed Area | Related Areas to Recheck | Reason | Source Status | Related Tickets |
|---|---|---|---|---|
| Task schedule or reminder configuration | Mobile Task List, FCM, Carer activity, SMS, email, alarm escalation | Schedule changes may affect task timing and downstream notifications | Confirmed | MA-2136 |
| Device Setup Steps | Service Request Process, Client File devices, CAMS/INS asset creation | Setup templates determine the runtime service-request workflow | Confirmed | SMAR-2652 |
| Service Request Type | Service Request create/edit, filtering, reports, permissions | Type changes may affect available workflow and reporting | QA Assumption | SMAR-2651 |
