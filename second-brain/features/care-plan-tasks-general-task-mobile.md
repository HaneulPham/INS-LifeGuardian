# Care Plan Tasks - General Task Mobile

This second-brain feature note points to durable logic for mobile creation and
lifecycle behavior of general Care Plan Tasks. Current Jira requirements,
confirmed BA decisions, verified API contracts, and verified current product
behavior take precedence.

## Primary context file

- `../../CARE_PLAN_TASKS_GENERAL_TASK_MOBILE_QA_CONTEXT.md`

## Source evidence

- `APP-MA-2136: Care Plan Tasks - Create General Task`
- Source type: Confluence PDF export containing existing test cases and
  expected behavior.
- Reviewed: 2026-07-03.

## Feature memory

- Mobile users create a general care plan task through a five-step flow:
  Create Selection, Task Style, Task Details, Schedules, Task Duration/Review.
- Task is not saved until the final Create Task action on Review Task.
- Supported styles are Simple, Instructions, Button Log, Checklist, and Grid.
- Simple, Instructions, and Button Log are one-schedule styles.
- Checklist and Grid support multiple schedules.
- Schedule recurrence supports Daily, Weekly, and Monthly.
- When multiple schedules exist, repeat type is locked so all schedules share
  the same occurrence type.
- Created tasks should appear in My Day / Task List on the correct effective
  date and sync across SOS app, Carer App, and CP Desktop where supported.
- Edit/delete behavior is constrained by posted occurrence/check-in history.

## Reusable risk reminders

- Draft steps accidentally creating backend task records.
- Create retry producing duplicate tasks.
- Style switch leaving hidden stale schedules in the payload.
- Repeat type mismatch across schedules.
- Date/time timezone shifts after save, refresh, or sync.
- Mobile and CP showing different task definition or check-in state.
- Edit/delete corrupting existing occurrence or outcome history.
- UI restrictions not enforced by API permissions.

## Open confirmations

- Exact API contract, methods, schema, response codes, and enum values.
- General task subtype and status values.
- Role/platform permission matrix for SOS app, Carer App, and CP Desktop.
- Notification/job behavior after successful create/update/delete.
- Audit/history/report/export behavior.
- Offline draft policy before final create.
