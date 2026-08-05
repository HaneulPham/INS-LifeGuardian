# Test data and cleanup

- Use non-production tenant/client data approved for automation.
- Generate unique, traceable data with ticket/case prefixes and timestamps or random suffixes.
- Prefer API setup over direct database writes unless database setup is an approved repository pattern.
- Register cleanup immediately after a resource is created.
- Run cleanup in reverse order and make it safe when a resource was only partially created or already removed.
- Never delete shared baseline data, real client records, or data not created by the test unless the approved scenario explicitly requires it and a protected fixture exists.
- For destructive, billing, alert, notification, queue, device, export, or durable-history flows, require an approved safe environment and explicit cleanup/rollback evidence.
- Report cleanup failures separately because they may contaminate later tests.
