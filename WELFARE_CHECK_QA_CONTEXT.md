# INS LifeGuardian Welfare Check QA Context

Use this document as supporting project knowledge when analyzing Welfare Check, Care Plan Task, Task Occurrence, notification, escalation, or Welfare Alarm changes.

This document summarizes supplied QA evidence. It is not a replacement for current Jira acceptance criteria, API contracts, or production configuration. Where the sources conflict, the item is explicitly marked `Needs confirmation`.

## Source documents

- SMAR-2363: Create Automated Welfare Checks
- SMAR-2475: CP - Prevent Schedule add/delete after Task Occurrences Posted
- SMAR-2489: Welfare Check - Close Alarm Message Wording
- Source PDFs were supplied and reviewed on 23/06/2026.

## Evidence interpretation

- Treat approved test intent and repeated behavior across the sources as strong project context.
- Do not treat a historical `PASS`, `FAIL`, `BLOCKED`, `REJECTED`, or `SKIP` result as proof of current production behavior.
- Test data, client identifiers, names, timestamps, build numbers, screenshots, and tokens are execution evidence rather than reusable business rules.
- Do not reuse client-identifying test data from the source documents in new outputs.
- When a source describes existing backend behavior that appears unsafe or inconsistent, preserve it as an open question rather than converting it into an expected requirement.

## Feature purpose

Automated Welfare Checks are Care Plan Tasks that create scheduled check-in opportunities for a client. A missed check-in can progress through due, reminder, and escalation stages. Configured channels may receive notifications, and escalation can raise a Welfare Alarm. A later successful check-in creates a Task Occurrence and resolves the outstanding workflow according to the last stage reached.

## Relevant platforms and components

- CP Desktop: task creation/editing, Care Plan Tasks, Alarm Dashboard, Alarm Details, and Alarm History.
- SOS App: task synchronization and client check-in.
- Carer App: configured reminder, escalation, and de-escalation activities.
- Backend task APIs and task-occurrence APIs.
- Background scheduling, reminder, escalation, and de-escalation processing.
- FCM/push, SMS, email, Village Contacts, Emergency Contacts, alarms, and notification/history records.

## Welfare Check task model

- API task `Type` is `Task` and `SubType` is `WelfareCheck` in the supplied examples.
- A new Welfare Check is expected to begin as active.
- A Welfare Check form includes task identity/content fields, a schedule section, reminder configuration, escalation configuration, UI style, and button text.
- The Welfare Check-specific fields are not expected on a General task form.
- `ButtonText` supports a default value and a custom value; the exact current default must be confirmed from the active requirement or API contract.
- A Welfare Check requires at least one schedule.

### Reminder channels

The supplied UI coverage includes:

- Carer App
- SMS Emergency Contacts
- SMS Village Contacts
- Email Village Contacts

`Alarm` is not a valid reminder channel in the supplied tests.

### Escalation channels

The supplied UI coverage includes:

- Alarm
- Carer App
- SMS Emergency Contacts
- SMS Village Contacts
- Email Village Contacts

### Village Contact configuration

- Village Contacts support the notification type `Welfare Check (Auto)`.
- Email and SMS notification rows can be configured separately.
- SMS and email delivery can be limited by configured From/To time windows.
- Removing a Welfare Check notification row must not remove or alter unrelated notification rows.

## Schedule configuration

Supported occurrence types in the supplied coverage are:

- Daily: Time Of Day
- Weekly: Time Of Day and Weekday
- Monthly: Time Of Day and Day Of Month

Welfare Check schedule coverage includes:

- Multiple schedules under one task.
- Duplicate schedule rejection.
- Overlap detection between schedules.
- Validation after reminder or escalation timing changes cause a previously valid schedule to overlap.
- Rejection of mixed occurrence types under one task when the same-occurrence rule is enforced.
- Refresh/reopen persistence and SOS App synchronization.

### Schedule duration boundaries

The supplied overlap matrix uses these occurrence-period limits:

- Daily: 1,440 minutes
- Weekly: 10,080 minutes
- Monthly: 44,640 minutes

The schedule window plus configured reminder/escalation timing must stay within the applicable occurrence period. Exact formulas and boundary inclusivity must be verified against the current implementation before new boundary cases are finalized.

## Lifecycle and timing behavior

### Timezone

- FCM and notification timing is based on the client's timezone.
- QA must compare the configured client timezone, backend timestamps, displayed local time, and notification delivery time.

### Stage progression

The supplied timing examples support this sequence:

1. Schedule due time is reached.
2. Reminder is processed after `RemindAfter` minutes.
3. Escalation is processed after `EscAfter` minutes from the reminder stage.

For example, a check due at 8:15 AM with 120 reminder minutes and 120 escalation minutes escalates at 12:15 PM. Confirm the calculation against the current job implementation when a requirement changes timing semantics.

### Check-in boundaries

- Before schedule start: check-in is rejected and no Task Occurrence or lifecycle side effect should be created.
- At due time: check-in is accepted and later reminder/escalation processing for that occurrence is suppressed.
- After reminder: check-in is accepted, a Task Occurrence is created, and the outstanding reminder-stage workflow is resolved without continuing to escalation.
- At the escalation boundary: ordering and race behavior must be tested for exactly-once results.
- After escalation: check-in is accepted, a Task Occurrence is created, and the outstanding escalation/Welfare Alarm workflow is resolved.
- Retrying the same occurrence after resolution must not create duplicate de-escalation or contact notifications.

### Recurrence and completion

- Daily, multi-daily, weekly, and monthly recurrence are covered.
- The next valid occurrence is generated according to schedule and date range.
- Monthly schedules require explicit coverage for months that do not contain the configured day.
- After the last valid occurrence/end-date behavior is completed, no next occurrence is generated.
- The UI may present the task as `Completed` while supplied API examples use backend status `Disabled`; exact status mapping must be confirmed.

## Notification behavior

Depending on configuration and lifecycle stage, the supplied suites cover:

- `TaskDue` FCM to the SOS App.
- `TaskReminder` through enabled reminder channels.
- `TaskEscalation` through enabled escalation channels.
- `TaskDeEscalation` or equivalent resolution behavior after a post-reminder or post-escalation check-in.
- Channel-specific non-delivery when a channel is not selected.
- SMS/email delivery-window enforcement for Village Contacts.
- No duplicate delivery when an occurrence request is retried.

Every notification assertion should verify recipient, channel, stage, client, schedule name, local time, message content, log/history record, and duplicate prevention.

## Welfare Alarm behavior

### Alarm creation

- An enabled `Alarm` escalation channel raises a Welfare Alarm when the client misses the check-in through escalation time.
- Expected initial alarm status is `Open`.
- Expected alarm type is `Welfare Alarm`/`WelfareAlarm`; the exact UI/API label mapping requires confirmation.
- Source/client mapping must select the correct client UUID, including a file containing multiple clients.
- One escalation event must not create duplicate alarms or an alarm for another client in the same file.

### Escalation message

The supplied expected template is:

`{{ClientName}} has missed their Welfare Check scheduled for {{ScheduleName}} at {{NextDueDateTime}}.`

Verify the same client, schedule, and localized due time across Alarm Dashboard, Alarm Details, Alarm History, and related notifications.

### Automatic closure after check-in

- A successful check-in after escalation automatically closes the open Welfare Alarm.
- Alarm status moves from `Open` to `Closed` without manual intervention.
- The Task Occurrence is created before or as part of resolving the escalation workflow.
- Alarm History retains the closure and outcome description.
- The intended automatic closure template is based on client, schedule, and check-in time, but the supplied SMAR-2489 example contains an AM/PM inconsistency and must not be copied as authoritative wording.

### Manual closure

- A CP user can take and manually close an open Welfare Alarm.
- The selected outcome and any entered Outcome Details are saved to Alarm History.
- Manual closure does not create a synthetic client check-in.
- A client may still check in for the missed schedule after manual alarm closure.
- That later check-in creates the Task Occurrence but must not reopen the alarm.
- The later check-in must not overwrite the manually selected outcome or Outcome Details.
- No duplicate alarm or automatic resolution message should replace manual closure history.

## Editing and schedule locking

### Before any Task Occurrence exists

- Schedule items can be added, edited, and deleted.
- The saved schedule must persist after reopen and synchronize to the SOS App.
- Deleting every schedule is rejected.

### After at least one Task Occurrence is posted/completed

- Schedule items cannot be added, edited, or deleted.
- A request combining allowed general-field updates with a blocked schedule change rejects the update rather than partially saving the schedule mutation.
- Persisted schedule data remains unchanged after a rejected UI or API attempt.
- Supported non-schedule fields can still be edited when the schedule is submitted unchanged. The supplied tests include task name, instructions, and Welfare Check reminder/escalation configuration.

### Validation wording requiring reconciliation

- CP test expectation: `Schedule cannot be modified after task creation`
- API test expectation: `Schedule cannot be modified after a task is completed`

These messages describe related locking behavior but are not textually consistent. Confirm the intended UI and API messages before writing exact-message assertions.

## Deletion and client/file restrictions

- An active Welfare Check with no posted/completed occurrence can be deleted.
- Deleting the task sends supported task-deletion synchronization to the SOS App.
- Deleting a task by itself must not behave like check-in, reminder, escalation, or de-escalation.
- A completed/disabled task with occurrence history cannot be deleted in the supplied coverage.
- Active Welfare Check tasks can block destructive client/file operations such as client deletion, file suspension, or file deletion. Confirm the exact scope and user-facing prompt for each operation.
- Historical Task Occurrences remain unchanged when task deletion is rejected.

## API map from supplied test evidence

### Task APIs

- Create: `POST {{domain}}/shm/task/v2`
- Get one: `GET {{domain}}/shm/task/v2/{ClientUuid}?CreAt={CreAt}`
- Get all for client: `GET {{domain}}/shm/task/v2/{ClientUuid}`
- Update: `PUT {{domain}}/shm/task/v2/{Uuid}?CreAt={CreAt}`
- Delete: `DELETE {{domain}}/shm/task/v2/{ClientUuid}?CreAt={CreAt}`

Path identity is not fully consistent between `ClientUuid` and `Uuid` in the supplied tests. Confirm the active OpenAPI/Postman definition before generating executable cases.

### Task Occurrence API

- Create: `POST {{domain}}/shm/taskoccurrence/v2`
- The supplied examples send an array of occurrence objects.
- Covered data includes `ClientUuid`, `FileUuid`, task `CreAt`, `TaskOccurrenceIndex`, and `Outcomes[]` containing matching schedule data.

### Expected response patterns

- Successful task and occurrence operations in the supplied suites generally expect `200 OK`, including creation.
- Validation failures generally expect `400 Bad Request`.
- Missing client/file/task references generally expect `404 Not Found`.
- Exact status codes and error schemas must be confirmed from the active API contract rather than generalized from these test exports.

### Notable payload fields

Supplied task examples include:

- `ClientUuid`, `FileUuid`, `CreAt`
- `Title`, `Instructions`, `StartAt`, `EndAt`
- `Type`, `SubType`, `Status`, `Category`
- `Occurrence`, `Schedules[]`
- `ScheduleName`, `ScheduleTime.Hours`, `ScheduleTime.Minutes`, and occurrence-specific schedule fields
- `RemindAfter`, `RemindType[]`, `EscAfter`, `EscType[]`
- `Style`, `ButtonText`, `ImpactsAdherence`
- Creator/updater audit fields

Do not assume every field is client-supplied, editable, or required without the current schema.

## Confirmed validation themes

- Required task identity and relationship fields.
- At least one schedule for a Welfare Check.
- Required positive reminder/escalation timing and at least one applicable channel.
- Numeric type and boundary validation for reminder/escalation values.
- Schedule hour/minute, weekday, day-of-month, occurrence enum, duplication, and overlap validation.
- Valid client/file ownership and active availability.
- Immutable task type/subtype where applicable.
- Completed/disabled task update and delete restrictions.
- Empty occurrence array and empty outcomes rejection.
- UUID, timestamp, occurrence index, and schedule-reference validation.
- No unintended persistence or integration side effects after rejected requests.

## Open questions and source conflicts

1. **Task endpoint namespace:** SMAR-2475 contains `/lg/task/v2/`; SMAR-2363 primarily uses `/shm/task/v2`. Determine whether `/lg` is legacy, erroneous, or environment-specific.
2. **Schedule lock wording:** CP and API expected messages differ, as recorded above.
3. **Automatic-close time wording:** one SMAR-2489 case checks in at 12:25 PM but expects 12:25 AM in the outcome text.
4. **Status terminology:** clarify UI `Completed` versus API `Disabled` and whether these represent the same lifecycle state.
5. **Escalation calculation:** source examples support cumulative reminder-then-escalation timing; confirm the job contract and boundary ordering.
6. **Schedule identity validation:** one supplied API case records acceptance of an invalid/cross-task `Outcomes.ScheduleUuid` without ownership validation. Treat this as observed behavior or a potential defect, not a desired rule, until confirmed.
7. **Occurrence for deleted task:** one supplied API case accepts an occurrence referencing a deleted task while suppressing downstream processing. Confirm whether this is intended compatibility behavior.
8. **Creation response code:** supplied cases use `200 OK`; do not assume `201 Created` for these APIs without contract evidence.
9. **Current execution status:** test results span different builds and include earlier FAIL/BLOCKED results followed by PASS. Revalidate against the target build.

## Required QA posture for future Welfare Check work

- Build an explicit timeline for due, reminder, escalation, check-in, job execution, and notification delivery.
- Include exact boundary and race cases, especially check-in at reminder/escalation time.
- Separate UI state, API response, persisted task/occurrence state, alarm state, and notification/job side effects.
- Verify exactly-once behavior for Task Occurrence, alarm creation/closure, activity, SMS, email, FCM, and history.
- Cover client timezone, day rollover, DST where applicable, delayed queues, retries, and out-of-order processing.
- Cover single-client and multi-client file mapping.
- Preserve manual alarm outcomes when a later automated event arrives.
- Verify negative requests cause no partial persistence or downstream delivery.
- Use the current requirement/API contract for exact fields, messages, and status codes when it conflicts with this historical QA evidence.
