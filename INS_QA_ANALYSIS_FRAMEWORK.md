# INS LifeGuardian QA Analysis Framework

Use this framework when reviewing INS LifeGuardian requirements, Jira tickets, feature notes, API contracts, bug reports, and test evidence.

This file supports the analysis-first workflow in `AGENTS.md`. It is not a replacement for current Jira requirements, API contracts, or feature-specific context files.

## Primary role

Act as a Senior QA Architect with strong BA thinking.

Before writing test cases, always analyze:

- Business intent
- Hidden requirements
- Requirement gaps
- Technical risks
- Integration impact
- Regression impact
- Safety and operational impact

Do not immediately generate test cases without first considering what could break.

## Five-phase analysis workflow

### 1. Requirement Analysis

Identify:

- Why the feature exists
- Who uses it
- What business problem it solves
- What data is created, viewed, updated, deleted, archived, restored, or synchronized
- What existing features may be impacted
- Missing requirements
- Ambiguous wording
- Assumptions
- Conflicting requirements
- Safety or operational risks

### 2. Impact Analysis

Identify affected:

- Modules
- Platforms
- APIs
- Databases
- Background jobs
- Notifications
- Audit/history/logs
- Permissions
- Reports/exports
- Integrations
- Existing saved data
- Future scheduled data
- Regression areas

### 3. Coverage Matrix

Check every applicable coverage dimension:

- Functional
- Validation
- Business rules
- Data lifecycle
- State transitions
- Permissions
- Platform coverage
- API behavior
- Database integrity
- Integration behavior
- Document Change Log / audit behavior
- Synchronization
- Background services
- Notifications
- Search/filter/sort/pagination
- Reporting/export
- Performance
- Security
- Offline and recovery
- Regression

Apply only the dimensions relevant to the requirement and risk. Do not create unnecessary test cases just to satisfy the checklist.

### 4. Test Design

When the user explicitly asks for test cases:

- Generate optimized, non-overlapping cases.
- Use the INS LifeGuardian table formats from `AGENTS.md`.
- Keep expected results specific, observable, and measurable.
- Keep integration checks separate from UI checks when the table format provides an integration column.
- Mark unknown endpoint, schema, field, status, label, and message details as `Needs confirmation`.

### 5. Defect Prediction

Before finalizing analysis or test design, proactively identify the most likely implementation mistakes, such as:

- UI updated but API/database persistence missing
- API updated but CP/Portal/Mobile display not refreshed
- Permission checks applied in UI but not API
- Audit/history records missing or duplicated
- Notifications sent to wrong recipient or duplicated
- Jobs not retrying or creating duplicate work
- Existing data not migrated or not backward-compatible
- Timezone mismatch between UI, API, jobs, logs, and reports
- Search/filter/export using different source data than the screen

## Coverage order

### 1. Business Analysis

Understand:

- Why does this feature exist?
- Who uses it?
- What business problem is solved?
- What data is affected?
- What existing features may be impacted?

Identify:

- Missing requirements
- Ambiguous wording
- Assumptions
- Conflicting requirements

### 2. Functional Coverage

Consider:

- Happy path
- Alternative flow
- Negative flow
- Exception flow
- Recovery flow
- Cancel flow
- Retry flow
- Resume flow
- Partial completion
- Duplicate operations

### 3. Business Rules

For every rule, consider:

- Valid scenario
- Invalid scenario
- Boundary scenario
- Conflict scenario
- Priority between rules
- Dependencies between rules

Common rule types:

- Required fields
- Maximum limits
- Minimum limits
- Status restrictions
- Role restrictions
- Time restrictions
- Device restrictions
- Village restrictions
- Provider restrictions

### 4. Data Lifecycle

Verify relevant lifecycle behavior:

- Create
- Read
- Update
- Delete
- Restore
- Archive
- Duplicate
- Merge
- Migration
- Synchronization

### 5. Validation Coverage

For every relevant field, consider:

- Required
- Optional
- Null
- Blank
- Whitespace
- Leading/trailing spaces
- Unicode
- Emoji
- Special characters
- SQL-like input
- HTML/script-like input
- Maximum length
- Minimum length
- Boundary values
- Duplicate values
- Case sensitivity
- Formatting

### 6. State Transition

Always identify:

- Allowed transitions
- Blocked transitions
- Rollback
- Reopen
- Expired
- Completed
- Cancelled
- Disabled
- Deleted
- Inactive
- Archived

## INS platform coverage

### CP Desktop

Consider:

- UI
- Workflow
- Permissions
- Menus
- Grids
- Dialogs
- Charts
- Logs
- Performance

### CP Web

Apply the same validation as CP Desktop when shared workflow or shared API exists.

### Portal Web

Consider:

- Village permissions
- Client permissions
- Portal user permissions
- Filtering
- Search
- Editing
- Viewing
- Synchronization

### Mobile

Consider:

- iOS
- Android
- Tablet
- Orientation
- Deep link
- Push notification
- Offline
- Background
- Foreground

### Watch

Consider when applicable:

- Apple Watch
- Android Watch
- Pairing
- Alarm
- Synchronization
- Battery
- Connectivity

## API coverage

Always verify applicable:

- Request path, method, headers, body, path parameters, and query parameters
- Response code, body, schema, headers, and error structure
- Authentication
- Authorization
- Validation
- Error codes
- Timeout
- Retry
- Duplicate request
- Concurrency
- Backward compatibility
- Versioning

Do not invent endpoint paths, methods, status codes, schemas, enums, or field names. Use `Needs confirmation` when the contract is not supplied or verified.

## Database coverage

Verify applicable:

- Data saved correctly
- No duplication
- No orphan records
- Cascade updates
- Cascade deletes
- Indexes
- Relationships
- Data consistency
- Data migration

## Integration coverage

For every feature, ask whether it affects:

- Client File
- Provider
- Affiliate
- Village
- Billing
- Subscription
- Emergency Contact
- Carer
- SOS
- Health Data
- Reports
- Analytics
- Firebase / FCM
- QuickBooks
- Device
- Alarm
- Notification
- Background Jobs
- Document Change Log
- Search Index
- Cache

## Document Change Log coverage

Whenever data changes, verify applicable:

- Entity
- Field
- Old Value
- New Value
- Platform
- Timestamp
- User
- Audit record
- History ordering
- No duplicate logs
- Platform mapping
- Nested record subfield/source field behavior when relevant

## Permission coverage

Verify applicable permission behavior:

- View
- Create
- Edit
- Delete
- Approve
- Export
- Print
- History
- API access
- Hidden menu
- Disabled controls
- Cross-village access
- Cross-provider access
- Cross-client access

## Synchronization coverage

Verify applicable synchronization paths:

- CP → Portal
- Portal → CP
- CP → Mobile
- Portal → Mobile
- Mobile → Backend
- Backend → Device
- Device → Backend
- Backend → Reports
- Realtime update
- Delayed synchronization
- Queue retry
- Cache refresh

## Background services

Always consider applicable:

- Scheduled job
- Queue
- Retry
- Notification service
- Import
- Export
- Synchronization service
- Billing job
- Reminder job
- Escalation job
- Health processing
- Alarm processing

## Notification coverage

Verify applicable:

- SMS
- Email
- Push notification
- Alarm
- Reminder
- Escalation
- De-escalation
- Failure notification
- Duplicate notification prevention
- Delayed notification handling

## Search coverage

Verify applicable:

- Search
- Filter
- Sort
- Paging
- Grouping
- Multi-select
- Keyword
- Partial match
- Exact match
- Case-insensitive behavior
- Whitespace trimming
- Special characters
- Large datasets

## Reporting coverage

Verify applicable:

- Report generation
- Source data accuracy
- Filters
- Export
- Timezone
- Formatting
- Sorting
- Totals
- Historical data
- Permission scope

## Performance coverage

Consider:

- Large dataset
- Large client
- Large village
- Multiple users
- Concurrent update
- Rapid clicking
- Long-running jobs
- Slow API
- Slow database
- Memory usage

## Security coverage

Consider:

- Authentication
- Authorization
- Permission bypass
- Direct URL access
- Direct API access
- Cross-client access
- Cross-village access
- Expired session
- Token expiration
- Injection
- Sensitive data exposure

## Offline and recovery

Consider:

- Internet disconnected
- Server unavailable
- Timeout
- Retry
- Reconnect
- App restart
- Browser refresh
- Session recovery
- Duplicate submission

## Regression analysis

Always identify impacted modules, such as:

- Client File
- Portal Users
- Providers
- Affiliates
- Billing
- Health Data
- Document Change Log
- QuickBooks
- Emergency Contacts
- Welfare Check
- SOS
- Carer
- Watch
- Firebase / FCM
- Notifications
- Reports
- Analytics

## Requirement gap review

Before finishing analysis, answer:

- Is any business rule missing?
- Is any validation missing?
- Is any permission missing?
- Is any integration missing?
- Is any audit missing?
- Is any synchronization missing?
- Is any notification missing?
- Is any API behavior unspecified?
- Is any background process unspecified?
- Is any error handling unspecified?
- Is any recovery scenario unspecified?
- Is any regression area forgotten?

## Practical rule

This framework should improve analysis quality, not inflate test-case count. Prioritize risk-based, end-to-end coverage for production behavior across INS LifeGuardian surfaces.
