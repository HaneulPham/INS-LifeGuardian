# INS LifeGuardian QA Project Constants

Use this file for stable project-wide QA conventions. `AGENTS.md`, current
approved Jira acceptance criteria, and published API contracts remain the
governing instructions and evidence sources.

Do not convert an unknown value into a project rule. Keep it marked
`Needs confirmation` until an authorized source confirms it.

## Source and traceability

- Requirement identifier: Jira issue key when available
- Requirement version: Jira updated date or named specification version
- API contract version/source: `Needs confirmation`
- Design source/version: `Needs confirmation`
- Test evidence location and retention period: `Needs confirmation`

Every formal requirement review, test suite, regression plan, or QA handover
should identify the applicable issue/specification and its version or updated
date when available.

## Environments

| Purpose | Name/URL | Permitted data | External delivery | Status |
|---|---|---|---|---|
| Development | Needs confirmation | Synthetic/de-identified by default | Needs confirmation | Needs confirmation |
| QA/Test | Needs confirmation | Synthetic/de-identified by default | Sandbox or disabled by default; needs confirmation | Needs confirmation |
| Staging/UAT | Needs confirmation | Approved data only | Needs confirmation | Needs confirmation |
| Production | Needs confirmation | Authorized production data | Live—explicit authorization required | Needs confirmation |

Never include credentials, tokens, or private client data in this file.

## Severity definitions

The official severity model is `Needs confirmation`. Until confirmed, state
severity as a QA recommendation and use these provisional meanings:

- **Critical**: actual or credible risk to life/safety, emergency-response
  failure, widespread service outage, unrecoverable/cross-tenant data exposure,
  or critical financial/integration corruption with no safe workaround.
- **High**: a core workflow is blocked or materially incorrect; notifications,
  alarms, care tasks, permissions, billing, or data integrity are significantly
  affected; workaround is absent or operationally unsafe.
- **Medium**: partial functional failure with a reasonable workaround and no
  immediate safety or major data-integrity impact.
- **Low**: limited usability, presentation, or low-impact inconsistency that does
  not prevent the intended workflow.

## Priority definitions

The official delivery-priority model is `Needs confirmation`. Do not treat
severity and priority as interchangeable. Until product/engineering confirms
priority, label any value as a QA recommendation:

- **High**: immediate response/release blocker
- **Medium**: fix before the affected release or urgently patch
- **Low**: plan for an upcoming release
- **Lowest**: backlog/cosmetic or low operational impact

## Test-case identifiers

- Official ID pattern: `Needs confirmation`
- System of record for test cases: `Needs confirmation`
- Until confirmed, use clearly temporary sequential IDs scoped to the output,
  such as `WEB-TEMP-001`, `MOB-TEMP-001`, `API-TEMP-001`, and `REG-TEMP-001`.
- Replace temporary IDs before importing into the official test-management
  system.

## Supported platforms

| Surface | Supported versions/devices | Status |
|---|---|---|
| CP Desktop | Needs confirmation | Needs confirmation |
| CP Web browsers | Needs confirmation | Needs confirmation |
| Portal Web browsers | Needs confirmation | Needs confirmation |
| SOS Mobile iOS | Needs confirmation | Needs confirmation |
| SOS Mobile Android | Needs confirmation | Needs confirmation |
| Carer App iOS | Needs confirmation | Needs confirmation |
| Carer App Android | Needs confirmation | Needs confirmation |

Do not invent a browser, OS, handset, tablet, wearable, or desktop support range.
When the matrix is unavailable, select representative coverage only as a QA
recommendation and mark it `Needs confirmation`.

## Accessibility

- Required standard and conformance level: `Needs confirmation`
- Supported assistive technologies: `Needs confirmation`
- Required browser/assistive-technology combinations: `Needs confirmation`
- Until confirmed, report observable keyboard, focus, labeling, contrast,
  scaling, screen-reader, motion, and touch-target risks without claiming formal
  conformance.

## Locale, date, and time

- Primary business locale: `Needs confirmation`
- Primary business timezone: `Needs confirmation`
- Server/backend timezone: `Needs confirmation`
- Daylight-saving behavior: `Needs confirmation`
- General UI date/time conventions: `Needs confirmation`
- Confirmed Document Change Log date format: `dd/MM/yyyy`
- Confirmed Document Change Log notification-time format: 12-hour time with
  AM/PM

Do not treat the user's local timezone or the test device timezone as the
business timezone. Always identify local, business, server, and stored UTC time
when timing affects schedules, reminders, escalations, alarms, jobs, reports, or
audit history.

## Release and build identification

- Release naming/version convention: `Needs confirmation`
- CP Desktop build identifier location: `Needs confirmation`
- CP Web/Portal deployment identifier location: `Needs confirmation`
- Mobile app build/version identifier location: `Needs confirmation`
- Backend/API deployment identifier location: `Needs confirmation`
- Feature-flag source of truth: `Needs confirmation`

Bug reports and QA handovers should include the environment, platform, visible
application version/build, backend/API deployment version when available,
feature flags relevant to the scenario, and validation date/time.
