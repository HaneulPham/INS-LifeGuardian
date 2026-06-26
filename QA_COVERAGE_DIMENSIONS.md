# INS LifeGuardian QA Coverage Dimensions

Use this checklist when analyzing a new INS LifeGuardian requirement before writing test cases. It supports the analysis-first workflow in `AGENTS.md`.

The goal is to think in coverage dimensions first, then turn only the relevant risks and rules into practical QA scenarios.

## Core coverage checklist

| Area | Questions to ask |
| --- | --- |
| Functional | Does the feature work as described? |
| Validation | What inputs are valid, invalid, and boundary values? |
| Business Rules | Are all business rules enforced? |
| Permissions | Who can and cannot view, create, update, delete, export, or access the feature by API? |
| UI/UX | Are labels, fields, statuses, buttons, messages, and formatting clear and requirement-aligned? |
| Navigation | Can users reach, leave, cancel, refresh, reopen, and resume the feature correctly? |
| Data | Is data saved, updated, deleted, restored, and displayed correctly across sessions? |
| Integration | Do dependent systems receive the correct updates without duplicates? |
| Audit | Are history, logs, and change records created with correct old/new values, user, timestamp, and source? |
| Notification | Are SMS, email, push, alarms, reminders, and restorals sent to the right recipients at the right time? |
| Background Jobs | Are queues, scheduled jobs, retries, de-escalations, and duplicate prevention handled correctly? |
| API | Are request, response, validation, authorization, schema, and error handling covered? |
| Database | Is data integrity protected, including duplicates, cascades, nulls, and relationships? |
| Performance | Does behavior remain acceptable with large data, concurrency, slow responses, or repeated actions? |
| Security | Are authentication, authorization, token/session handling, tenant scope, injection, and direct access covered? |
| Offline / Network | What happens during internet loss, reconnect, timeout, retry, or mobile background/foreground transitions? |
| Upgrade / Existing Data | Does the change remain compatible with historical saved data and future scheduled data? |
| Regression | Which existing features, reports, integrations, and workflows must remain unaffected? |

## Recommended analysis order

### 1. Happy path

Confirm the main user scenario works end to end.

Usually this produces only 1-3 test cases.

### 2. Business rules

Turn every business rule into explicit positive and negative coverage.

Example rules:

```text
Age >= 18
Only Active client
Provider required
Maximum 10 devices
```

Example coverage:

- Age = 18
- Age = 17
- Inactive client
- Missing provider
- 11 devices

### 3. CRUD behavior

If the feature edits data, consider:

- Create
- Read
- Update
- Delete
- Restore, when supported
- Duplicate prevention
- Bulk behavior, when supported
- Cancel without saving
- Refresh/reopen persistence

### 4. Input validation

Review every editable field for relevant cases:

- Required
- Empty
- Null
- Minimum
- Maximum
- Boundary
- Special characters
- Unicode
- Emoji
- SQL-like input
- HTML/script-like input
- Long text
- Leading/trailing spaces
- Trim behavior
- Duplicate
- Case sensitivity

### 5. State transitions

For status-based features, map allowed and blocked transitions.

Example:

```text
Draft
↓
Pending
↓
Approved
↓
Completed
```

Example coverage:

- Draft → Pending
- Pending → Approved
- Approved → Completed
- Completed → Draft should be blocked unless explicitly supported
- Pending → Completed should be blocked unless explicitly supported

### 6. Permission matrix

For INS LifeGuardian, permissions must be treated as high-risk coverage.

Consider role and scope combinations such as:

- Admin
- Operator
- Portal User
- Village User
- Read-only user
- Disabled user
- Linked-client user
- Cross-village or cross-file user

For each relevant role, consider:

- View
- Create
- Update
- Delete
- Export
- View history/audit
- Direct URL access
- Direct API access

### 7. Integration and synchronization

If CP, Portal, mobile, backend, or external services are involved, check the downstream impact.

Potential downstream areas:

- CP Desktop / CP Web
- Portal Web
- Carer App
- SOS Mobile
- Watch or wearable workflows, when applicable
- Billing
- Reports and exports
- Document Change Log / Document Field History
- Firebase / FCM
- SMS / Twilio
- Email
- Backend APIs
- Jobs and queues
- Notification logs
- Activity history

## Practical reminder

Do not turn every checklist item into a test case automatically. Select coverage based on the requirement, feature risk, production impact, and confirmed system behavior. Mark unknown behavior as `Needs confirmation`.
