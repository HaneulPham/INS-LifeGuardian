# Bug report style

Use this order:

- Title
- Summary
- Environment
- Path
- Preconditions
- Steps to Reproduce
- Actual Result
- Expected Result
- Frequency
- Severity
- Priority
- Business / Safety Impact
- Evidence
- Notes

Use a searchable title and reproducible steps. Actual Result is observed behaviour; Expected Result comes from a requirement or confirmed business rule. Label inferred expectations as QA assumptions. Do not claim root cause without code, API/database, log, or developer evidence.

Treat **Severity** and **Priority** as separate decisions:

- Severity describes the consequence to client safety, data integrity, security, operations, billing, or supported functionality.
- Priority describes the urgency and order in which the defect should be addressed.

Record build, environment, role, device/OS/browser, frequency, screenshots/video/logs, safety and operational impact, notification/integration impact, data integrity, privacy exposure, and regression risk when supported. Redact client, health, contact, credential, and tenant-sensitive evidence unless it is strictly required and approved for the defect system.
