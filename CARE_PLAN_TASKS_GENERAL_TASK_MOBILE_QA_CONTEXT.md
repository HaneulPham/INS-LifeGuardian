# INS LifeGuardian Care Plan Tasks General Task Mobile QA Context

This file is supporting QA and BA evidence for INS LifeGuardian. Current Jira
requirements, confirmed BA decisions, verified API contracts, and verified
current product behavior take precedence over this note. When this note
conflicts with newer evidence, keep the conflict visible and mark the affected
behavior as `Needs confirmation`.

## Purpose and authority

- Feature area: Care Plan Tasks / General Task creation from mobile apps.
- Source ticket/document: `APP-MA-2136: Care Plan Tasks - Create General Task`
  Confluence PDF export, reviewed on 2026-07-03.
- Source type: test-case evidence and BA-style logic inferred from those test
  cases.
- Evidence strength: repeated QA evidence, not independently verified API
  contract.
- Primary use: help BA, QA, and developers understand the intended feature
  logic before writing new requirements, test cases, bugs, or regression scope.

## Source documents

- `APP-MA-2136_ Care Plan Tasks - Create General Task-030726-080226.pdf`
- PDF title: `MA-2136: Care Plan Tasks - Create General Task - MobileApps -
  Confluence`
- Major sections observed:
  - Group 1: Create care plan task workflow.
  - Group 2: Care Plan Screen / My Day / Task List.

## Evidence interpretation

- The document is treated as test evidence that expresses expected feature
  behavior.
- The behaviors below should be read as BA logic derived from the test cases.
- Exact backend schema, response codes, enum values, permission matrix,
  notification jobs, audit records, and offline policy remain `Needs
  confirmation` unless separately verified.
- No execution-specific client, file, UUID, or health data from the source was
  preserved here.

## Feature purpose

Allow mobile users to create a general care plan task for a client so the task
can appear on the client's My Day / Care Plan Task List, follow configured
schedules, support check-in or completion behavior, and remain synchronized
across supported platforms.

The feature supports operational care delivery by letting staff or carers define
scheduled client activities from mobile, then see and act on those tasks in the
daily care workflow.

## Platforms and components

Repeated QA evidence covers:

- SOS Mobile on iOS and Android.
- Carer App on iOS and Android.
- CP Desktop.
- Backend task APIs.
- My Day / Task List.
- Task occurrence or outcome records.
- Sync/refresh behavior between mobile apps and CP Desktop.

Potentially related but not fully defined in the supplied evidence:

- CP Web: `Needs confirmation`.
- Portal Web: `Needs confirmation`.
- Reports and exports: `Needs confirmation`.
- Audit/history/log views: `Needs confirmation`.
- Notification logs/jobs/queues: `Needs confirmation`.

## Roles and permissions

Repeated QA evidence expects the user to have permission to create care plan
tasks before entering the create flow.

Needs confirmation:

- Which SOS app roles can create, edit, delete, check in, or un-check a general
  task.
- Which Carer App roles can create, edit, delete, check in, or un-check a
  general task.
- Whether CP Desktop and mobile permission rules are identical.
- Whether direct API access enforces the same permissions and client/file scope
  as the UI.
- Whether linked-client, village, file, inactive client, or archived client
  scope changes restrict task visibility and actions.

## Terminology and data model

### User-facing terms

- Task.
- Goal.
- Task Style.
- Task Details.
- Schedules.
- Add Schedule.
- Edit Schedule.
- Delete Schedule.
- Task Duration.
- Review Task.
- Create Task.
- Task Created.
- My Day.
- Task List.
- Edit Task.
- Delete Task.

### Style / layout options

The create flow supports five general task styles:

- Simple.
- Instructions.
- Button Log.
- Checklist.
- Grid.

Style controls both display and schedule-count rules.

### Expected backend concepts

The source cases refer to the following task concepts:

- `ClientUuid`.
- `FileUuid`.
- `Title`.
- `Instructions`.
- `Style`.
- `Type`.
- `SubType`.
- `Status`.
- `StartAt`.
- `EndAt`.
- `Occurrence`.
- `Schedules`.
- `CreAt`.
- Task occurrence or outcome records.

These names come from the test evidence and require API confirmation before
being treated as the final contract.

## Workflows and state transitions

### Create workflow

The mobile create flow has five steps:

1. Create Selection.
2. Task Style.
3. Task Details.
4. Schedules.
5. Task Duration and Review.

Task data remains local draft state until the final Create Task action on the
Review Task screen.

Opening screens, selecting a style, entering details, adding schedules, editing
schedules, deleting unsaved schedules, navigating back, or canceling the flow
must not create or update a backend task.

### Create Selection

- The user chooses what they want to add.
- Task is selected by default.
- Goal is visible but disabled/locked/coming soon.
- Continue should proceed with Task only.
- Goal must not be selectable or creatable from this flow while locked.

Needs confirmation:

- Exact Goal disabled wording and whether Goal appears for all users.
- Whether Goal is backed by API support but disabled only in mobile UI.

### Task Style

- User selects one of the five task styles.
- Simple is selected by default.
- Preview, pro tip, and bottom action label update when style changes.
- Style selection is local draft data until final create.
- Repeated taps should not duplicate navigation or create multiple screens.

### Task Details

- Task Title is required.
- Instructions is optional.
- Valid non-whitespace Task Title enables progression to Schedules.
- Whitespace-only Task Title is invalid.
- Instructions alone must not enable progression when Task Title is empty.
- Preview updates live from Task Title and Instructions where the selected style
  supports those fields.
- Long title and long/multiline instructions should remain readable and must not
  overlap controls.

Needs confirmation:

- Final maximum Task Title length and whether mobile truncates, blocks, or lets
  backend validate over-limit values.
- Final maximum Instructions length and sanitization rules.
- Whether emoji and special characters are allowed in saved task data.

### Schedules

- At least one schedule is required.
- Empty schedule state disables Next Step.
- Add Schedule captures schedule name, reminder time, and repeat type.
- Daily, Weekly, and Monthly recurrence are supported.
- Schedule time displays in 12-hour AM/PM format.
- Weekly requires one weekday.
- Monthly requires one day of month.
- Schedule cards display name, time, repeat label, and actions.
- Schedule add/edit/delete remains draft-only before final create.

### Style-based schedule count

One-schedule styles:

- Simple.
- Instructions.
- Button Log.

Multi-schedule styles:

- Checklist.
- Grid.

For one-schedule styles:

- The first valid schedule can be added.
- Add Schedule becomes disabled after one schedule exists.
- Deleting the only schedule restores the empty state and re-enables Add
  Schedule.
- Final create must not submit multiple schedules.

For multi-schedule styles:

- Multiple schedules can be added.
- Schedule order follows product behavior, either created order or defined sort
  order: `Needs confirmation`.

If the user changes from a multi-schedule style to a one-schedule style:

- Existing multi-schedule draft schedules should be cleared.
- User must add a new valid schedule before continuing.
- Cleared schedules must not be submitted hidden in the final payload.

### Repeat locking

When multiple schedules exist, all schedules use the same repeat type.

- If Daily is established, Weekly and Monthly are locked for additional or
  edited schedules.
- If Weekly is established, Daily and Monthly are locked.
- If Monthly is established, Daily and Weekly are locked.
- Repeat type can be changed only when a single schedule exists.
- Schedule name and reminder time remain editable while repeat type is locked.
- For Weekly schedules, the selected weekday can be changed while keeping Weekly.
- For Monthly schedules, the selected day of month can be changed while keeping
  Monthly.

### Task Duration

- Start date defaults to Today.
- User can change Start date.
- End date options include:
  - No end date.
  - 1 Week.
  - 2 Weeks.
  - 1 Month.
  - 3 Months.
  - Custom date.
- Fixed end date options recalculate from the selected Start date.
- Review displays either Start date only or Start date to End date depending on
  the selected end option.

Needs confirmation:

- Exact date display format for mobile.
- Exact timezone used when converting Start date and End date for the API.
- Whether EndAt is omitted, null, or a sentinel value for No end date.
- Whether custom end date can be earlier than Start date and how validation is
  shown.

### Review and create

- Review Task is the final check before saving.
- Review shows selected style preview, Task Title, Instructions where supported,
  schedules, occurrence labels, schedule count, Start date, and End date.
- Viewing Review Task does not call create API.
- Create Task triggers backend creation once.
- Create action should be protected from repeated taps.
- On success, the app shows Task Created and then returns to Task List / My Day
  after a short delay.
- Created task appears once after refresh/reopen.

### Failure and retry

If backend create fails:

- User remains on Review Task.
- Draft data is preserved.
- Error state indicates create failure.
- User can retry.
- Failed create must not persist a task or schedule jobs.
- Successful retry creates exactly one task.

If network is unavailable:

- User remains on a recoverable screen.
- Draft data is preserved.
- Task must not appear in Task List before successful create.
- Retry after network restoration sends one valid create request.

Offline behavior before final create is not fully confirmed:

- Some cases allow local draft navigation while offline.
- Some cases allow a clear no-internet message instead.
- Final offline policy is `Needs confirmation`.

## UI behavior

Key UI rules inferred from the cases:

- Screens must avoid blank page, crash, infinite loading, and critical layout
  cut-off.
- Back navigation should preserve local draft where supported.
- Cancel exits the flow without creating data.
- Cancelled draft data should not reappear as a saved task.
- Preview content must not display stale placeholder text as saved content.
- Long text must wrap, scroll, or truncate safely according to design.
- Disabled and selected states must be visually distinguishable.
- Task and schedule labels should use user-facing wording, not raw API enum
  values.

Important user-facing messages from test evidence:

- `Task Created!`
- `Your task is live! You'll be reminded at the scheduled times going forward.`
- `No reminders yet. Tap below to add your first schedule.`
- `Repeat type is locked - all schedules must use the same type.`
- `Repeat type can't be changed when multiple schedules exist. Delete other schedules first, then edit the repeat type.`
- Create failure/no-internet/server-error messages appear in the cases but exact
  final copy is `Needs confirmation`.

## Backend and API behavior

Repeated QA evidence references:

- Create: `POST /shm/task/v2`.
- Update: `PUT /shm/task/v2/{ClientUuid}?CreAt={CreAt}` or equivalent.
- Delete: task API delete using task identity such as `ClientUuid` and `CreAt`.
- List/GET task data after create/update/delete to refresh mobile displays.
- Task occurrence/outcome APIs for check-in/un-check-in behavior.

Expected create payload themes:

- Client/file identity.
- Task title.
- Optional instructions.
- Selected style.
- `Type = Task`.
- Expected subtype for general task: `Needs confirmation`.
- Active status.
- Start date.
- End date or no-end-date representation.
- One task-level occurrence type.
- Schedule list with schedule name, hours, minutes, weekday or day of month when
  applicable.

Expected API behavior:

- No create/update/delete request before final save/delete confirmation.
- Failed create/update/delete must not persist false UI state.
- Retry should avoid duplicate task creation.
- Task list refresh should display backend-returned values consistently.
- Updating allowed fields must preserve task identity and existing occurrence
  history.
- Deleting a task must affect only the selected task.

Needs confirmation:

- Exact endpoint namespace if `/shm/task/v2` differs by environment.
- Exact HTTP methods for update/delete.
- Exact response codes.
- Exact request/response schema.
- Exact enum values for style, type, subtype, status, and occurrence.
- Idempotency behavior for timeout or partial create.
- Pagination/filter/sort behavior for task list retrieval.

## Jobs, queues, and timing

The cases repeatedly expect notification, reminder, escalation, and due jobs not
to be created during draft steps.

Expected timing:

- Task due/reminder/escalation or related jobs should be generated only after a
  successful create, according to backend scheduling rules.
- Failed create must not schedule due, reminder, escalation, email, SMS, FCM, or
  activity side effects.
- Success screen auto-navigates to Task List after a short delay.

Needs confirmation:

- Whether general tasks create `TaskDue`, `TaskReminder`, or `TaskEscalation`
  jobs.
- Whether all five styles use the same scheduling engine.
- Whether reminder time is local client time, device time, village time, or
  server time.
- Whether monthly day 29, 30, or 31 skips months without that date or rolls to
  another day.

## Notifications and integrations

Repeated QA evidence expects no task update FCM, reminder, escalation, SMS,
email, or background job side effects before successful create/update/delete.

Needs confirmation:

- Whether general task creation sends FCM, silent sync notification, SMS, or
  email.
- Whether edit/delete triggers silent refresh notifications to SOS app, Carer
  App, or CP Desktop.
- Where notification delivery attempts and failures are logged.
- Whether external integrations consume general task data.

## My Day, task list, and cross-platform sync

After successful create:

- Created task appears on the correct effective date in My Day / Task List.
- Displayed values should match the saved title, instructions, style,
  occurrence, schedules, Start date, and End date.
- Task must not duplicate after refresh, reopen, retry, or date navigation.
- Task created from SOS app should appear in Carer App and CP Desktop where
  supported.
- Task created from CP Desktop should appear in SOS app for the same client/file
  where supported.

Check-in/un-check-in behavior:

- Check-in/completion state should sync across SOS app, Carer App, and CP
  Desktop.
- Un-check-in should remove or update completion state without corrupting other
  schedules or occurrences.
- Existing posted/check-in history must remain linked to the same task/schedule
  identity after allowed edits.

Needs confirmation:

- Whether Carer App can create tasks or only view/check in/edit/delete.
- Exact CP Desktop field support for mobile-created style/instructions.
- Whether My Day displays tasks by Start date, schedule date, occurrence date,
  or a combined effective-date rule.

## Edit task logic

Edit flow starts from Task Details and skips Task Style.

Expected rules:

- Existing task style cannot be changed in edit flow.
- Allowed edits may include Task Title and Schedule Name.
- For active tasks without posted/check-in occurrence history, schedule edits
  follow normal style and schedule-count rules.
- For tasks with posted schedule/check-in occurrence history:
  - Task Title can be edited.
  - Schedule Name can be edited.
  - Schedule identity must remain the same.
  - Adding schedules is blocked.
  - Deleting schedules is blocked.
  - Changing schedule time, repeat type, weekday, or day of month is blocked.
  - Existing occurrence/outcome history remains unchanged.
- Expired or completed tasks cannot be edited.
- Cancel/back exits without saving unsaved edit changes.
- Failed update keeps the draft available but must not display false success.

Needs confirmation:

- Full list of editable fields for tasks with and without posted occurrence
  history.
- Exact blocked-edit messages.
- Whether Start date and End date can be edited after creation.
- Whether edit restrictions are enforced equally by UI and API.

## Delete task logic

Eligible tasks can be deleted only after user confirmation.

Expected delete rules:

- Confirmation is shown before permanent delete.
- Cancel keeps the task visible.
- Confirmed delete removes the task from active task lists after refresh/sync.
- Delete applies only to the selected task.
- Other tasks for the same client/file remain unchanged.
- Deleted task cannot be checked in, unchecked, edited, or deleted again from
  stale UI.

Blocked delete scenarios:

- Task has at least one posted schedule occurrence.
- Task has at least one completed/check-in schedule.
- Task is expired/completed.

Failed delete behavior:

- Failed delete must not remove the task from UI or backend.
- Existing occurrence/outcome history is preserved.
- User can retry after network/backend recovery.

Needs confirmation:

- Exact task state field used to identify expired/completed tasks.
- Whether delete is hard delete, soft delete, or active-list exclusion.
- Where delete audit/history is recorded.

## Reports, exports, audit, and history

The supplied evidence focuses on mobile/CP task behavior and backend
persistence. It does not confirm report/export or audit/history behavior.

Needs confirmation:

- Whether create, update, delete, check-in, and un-check-in create audit/history
  records.
- Whether history captures modifier, timestamp, platform, old values, and new
  values.
- Whether task changes appear in reports/exports.
- Whether deleted tasks appear in historical reports.

## Data integrity and security

Critical integrity expectations:

- Draft steps must not create backend data.
- Create retry must not duplicate tasks.
- Style changes must not leave stale hidden schedules.
- Repeat type locking must keep a single task-level occurrence type.
- Date/time values must not shift after API save, refresh, or cross-platform
  sync.
- Edit restrictions must protect posted occurrence/check-in history.
- Delete restrictions must protect historical occurrence/outcome records.
- Cross-platform refresh must not show stale old task names, schedules, or
  completion state.

Security expectations:

- User must only create/edit/delete tasks for allowed client/file scope.
- UI restrictions must be enforced by backend APIs.
- Stale UI actions after delete or permission change should be rejected safely.
- Cross-client or cross-tenant leakage is a high-risk defect.

## Confirmed validation themes

Derived from repeated test-case coverage:

- Required Task Title.
- Whitespace-only Task Title invalid.
- Instructions optional.
- At least one schedule required.
- Schedule Name required.
- Reminder time required and displayed in 12-hour AM/PM format.
- Weekly requires a weekday.
- Monthly requires a day of month.
- One-schedule style cannot submit multiple schedules.
- Repeat type is locked when multiple schedules exist.
- Final create is the first point where backend creation should occur.
- Failed create/update/delete must not persist false success.

## Open questions and source conflicts

Critical:

- What exact roles and platforms can create, edit, delete, check in, and
  un-check general tasks?
- What is the final API contract for create, update, delete, list, and
  occurrence APIs?
- What subtype identifies a general task in backend data?
- What job/notification behavior is expected after successful create?
- What audit/history records are required for create, update, delete,
  check-in, and un-check-in?

Important:

- Is offline draft navigation supported before final create, or should offline
  be blocked earlier?
- What is the exact timezone basis for StartAt, EndAt, schedule hours/minutes,
  and My Day date selection?
- How should monthly schedules behave when the selected day does not exist in a
  month?
- Are reports/exports affected by mobile-created general tasks?
- Is CP Web or Portal Web in scope for display, edit, history, reports, or
  permissions?

Optional:

- Final wording for disabled Goal, locked repeat type, blocked edit/delete, and
  create/update/delete failures.
- Exact accessibility requirements for screen reader focus and dynamic text.

## Required QA posture

When analyzing future Care Plan Task / General Task tickets:

- Treat this file as supporting feature memory, not final authority.
- Read current Jira and API contract first when available.
- Separate BA-confirmed logic from test-evidence-derived behavior.
- Do not invent missing endpoint schema, enum values, response codes,
  notification messages, permission rules, or audit details.
- Focus on data integrity, duplicate prevention, schedule occurrence logic,
  cross-platform sync, task occurrence history, jobs/queues, permissions, and
  refresh/reopen persistence.
- For test cases, keep web/mobile/API/regression formats consistent with
  `AGENTS.md`.
