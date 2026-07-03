# INS LifeGuardian QA Risk Patterns

Use this file to remember repeated defect patterns and high-risk areas.

## High-risk patterns

### UI saves but backend persistence is incomplete

Risk:

- Screen shows updated data, but API/database/report/export still uses the old value.

Check:

- Refresh/reopen the screen.
- Verify API/backend persistence when available.
- Verify reports/exports if the field is reportable.

### UI permission exists but API permission is missing

Risk:

- Button/menu is hidden in UI, but direct API request still allows unauthorized access.

Check:

- Test UI permission.
- Test direct URL/API access when endpoint is known.
- Test cross-village, cross-client, and linked-client scope.

### CP updates but Portal/Mobile does not sync

Risk:

- Data is correct in CP but stale or missing in Portal, SOS Mobile, or Carer App.

Check:

- CP → Portal sync.
- CP → Mobile sync.
- Refresh/reopen behavior.
- Cache behavior and delayed synchronization.

### Audit/history/log missing or duplicated

Risk:

- Data changes are not traceable, or one user action creates duplicate records.

Check:

- Old Value / New Value.
- User/modifier.
- Timestamp/timezone.
- Source platform.
- No-change save behavior.
- Duplicate prevention.

### Notifications/jobs duplicate or use wrong recipient

Risk:

- SMS, email, push, alarm, reminder, escalation, or de-escalation is sent twice or to the wrong recipient.

Check:

- Recipient rules.
- Message title/body/placeholders.
- Job schedule.
- Retry behavior.
- Notification logs.
- Duplicate prevention.

### Timezone mismatch

Risk:

- UI, API, jobs, logs, and reports show different dates/times.

Check:

- Local display format.
- Server/API storage.
- Job execution time.
- Audit/report timestamp.
- Boundary times such as midnight, noon, DST, and month end when relevant.

### Existing data compatibility missed

Risk:

- New behavior works only for newly created records and fails for historical records.

Check:

- Existing saved data.
- Future scheduled data.
- Archived/inactive/deleted records when relevant.
- Migration/backfill expectation.
