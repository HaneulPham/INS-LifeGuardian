# Care Plan Tasks — Product Knowledge

## Platforms

- Mobile SOS iOS/Android
- Mobile Carer iOS/Android
- CP Desktop
- CP Web
- Backend APIs

## Confirmed Workflow

Create Task flow:
1. Style
2. Details
3. Schedules
4. Durations
5. Review & Create

## Confirmed Business Rules

- Styles: Simple, Instruction, Button Log, Checklist, Grid.
- Simple, Instruction, and Button Log allow only one schedule.
- Checklist and Grid allow multiple schedules.
- At least one schedule is required.
- Duplicate schedules are allowed.
- Delete schedule is immediate and has no confirmation.
- Current-day future check-in is allowed.
- Future-day check-in is blocked.
- Posted schedule cannot be deleted.
- Task name and schedule name can still be edited when posted schedule exists.

## Regression Areas

- Task List sorting
- Pull-to-refresh
- Cross-device sync
- SOS ↔ Carer ↔ CP sync
- Check-in / undo check-in
- Delete task
- Edit task
- Relogin
- Offline/reconnect
- Notification delivery
- Activity/task occurrence history

## Common Test Focus

- Create task by style
- Schedule validation
- Posted schedule rule
- Check-in rule
- Pull-to-refresh sync
- Multi-device behavior
- Backend failure
- Network failure

## Knowledge Status

| Item | Status | Source | Last Updated | Notes |
|---|---|---|---|---|
| Create Task has 5 steps: Style, Details, Schedules, Durations, Review & Create | Confirmed | MA-2136 QA review | 2026-07-17 | Used for mobile task creation test cases |
| Current-day future check-in is allowed | Confirmed | MA-2136 QA feedback | 2026-07-17 | Future-day check-in remains blocked |
| Posted schedule cannot be deleted | Confirmed | MA-2136 QA feedback | 2026-07-17 | User may still edit task name and schedule name |
| Audit history for task edit | Open Question | Missing requirement | 2026-07-17 | Need BA/Dev confirmation if activity history records edit details |
