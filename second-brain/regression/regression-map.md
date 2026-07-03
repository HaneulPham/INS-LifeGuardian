# INS LifeGuardian Regression Map

Use this file to map common regression areas when analyzing tickets.

## Core regression surfaces

| Area | Regression focus |
| --- | --- |
| CP Desktop / CP Web | UI workflow, permissions, grids, dialogs, save/cancel/refresh/reopen, logs |
| Portal Web | Village/client scope, linked users, permissions, search/filter/sort/pagination, sync |
| SOS Mobile | Mobile display, offline/online behavior, background/foreground, push/deep-link behavior |
| Carer App | Task/welfare/activity display, sync, notification behavior |
| Backend APIs | Auth, authorization, validation, persistence, idempotency, error handling |
| Jobs / Queues | Scheduling, retry, duplicate prevention, delayed execution |
| Notifications | Recipient, channel, title/body/placeholders, logs, duplicate prevention |
| Audit / History / Logs | Old/new values, source platform, user, timestamp, duplicate/no-change behavior |
| Reports / Exports | Source data, filters, sorting, timezone, formatting, permission scope |
| Integrations | FCM, SMS, email, Twilio, QuickBooks, device services, sync services |

## Release risk tags

- Must test before release
- Should test if time allows
- Regression only
- Automation candidate
- Manual only due to device/job/integration dependency
