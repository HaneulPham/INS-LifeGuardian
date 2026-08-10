# Billing and Reports — Product Knowledge

## Platforms

- CP Desktop
- CP Web
- Backend APIs
- Background jobs and EventBridge schedules
- Billing Reports
- QuickBooks integration

## Confirmed Hardware Rental Rules

- Hardware Rental uses a required 12- or 24-month Rental Term instead of an editable End Date in its billing-status dialog.
- The billing grid retains the End Date column and non-Hardware services retain their existing End Date behavior.
- Start Date and Rental Term derive the persisted Hardware Rental End Date.
- Hardware Rental remains Online through its End Date and changes Offline only after that date completes in the configured business time zone.
- One traceable automatic-Offline schedule is created for an Online Hardware Rental; term/date changes replace it and manual Offline cancels it.
- Eligible Hardware Rental occurrences appear in Village, Provider or Client Billing Reports without duplicate rows.
- QuickBooks Activity is `HARDWARE RENTAL`; descriptions use the approved billing-party format, term and payment sequence.

## Confirmed DVA Prior Approval Number Rules

- Work Orders and Invoices reject normalized exact `N/A`, `NA`, and `None` Prior Approval Number values case-insensitively in CP Web and the API.
- A supplied whitespace-only value is invalid, while a genuinely empty optional value remains allowed.
- Leading and trailing whitespace is trimmed before persistence; internal characters and variable valid free-text formats remain unchanged.
- Invalid API input returns HTTP `400 Bad Request` with `Error = "bad_request"` and `ErrorDescription = "'Dva Presc On' must be a valid value or blank"`.
- Historical invalid values remain viewable but must be corrected or cleared before an affected Work Order or Invoice update can persist.
- Final CP Web invalid-input presentation and exact message remain unresolved because current Jira and approved Confluence evidence conflict.

## Regression Areas

- Billing Service Status dialog and existing End Date workflows.
- Monitoring and other non-Hardware recurring services.
- Billing API persistence, authorization, tenant/client targeting and duplicate prevention.
- Client File Device Information Village Rental labels and unrelated fields.
- EventBridge schedule creation, replacement, cancellation, timing and retry observability.
- Village, Provider and Client Billing Reports, filters, calculations and regeneration.
- Monitoring, SIM, Welfare Check, Establishment Fee and Hardware Purchase report/export behavior.
- QuickBooks item mappings, invoice descriptions, occurrence sequence and duplicate export protection.
- Work Order create/update and Invoice update optional-value, exact-match, case-insensitive, whitespace, free-text, atomic-rejection, and historical-correction behavior.
- CP Web/API convergence for persisted Prior Approval Number values and protection of Invoice status, totals, payment state, and export state.
- SMAR-2633 DVA rental-date generation and XML export using supported Presc On data.

## Knowledge Status

| Knowledge Item | Source Status | Source / Evidence | Last Updated | Notes |
|---|---|---|---|---|
| Hardware Rental term, End Date and automatic-Offline lifecycle | Confirmed | Jira SMAR-2467; approved Confluence page 2581889038 v28 | 2026-08-05 | Reusable CP Desktop, API and scheduler behavior |
| Hardware Rental Billing Report and QuickBooks mapping | Confirmed | Jira SMAR-2467; Confluence pages 2581889038 v28 and 2438201345 v6 | 2026-08-05 | Village and Provider/Client report/export paths |
| Exact Billing API and EventBridge field-level contracts | Open Question | Not supplied in reviewed Jira or Confluence evidence | 2026-08-05 | Use implemented contract and developer-supported evidence; do not hardcode unknown fields |
| DVA Prior Approval Number invalid list, whitespace distinction, trimming, affected records, and API 400 contract | Confirmed | Jira SMAR-2528 current description; Confluence page 2628780034 v10 | 2026-08-10 | Reusable Work Order and Invoice validation behavior |
| CP Web invalid-input presentation and exact message for Prior Approval Number | Conflict | Jira SMAR-2528 description and comment 44529; Confluence page 2628780034 v10 | 2026-08-10 | Resolve error display versus field clearing and `Presc On.` versus `Dva Presc On` wording before activating deferred UI cases |
| Work Order/Invoice route methods and successful API response contracts for SMAR-2528 | Open Question | Confluence assumptions A1–A3; successful response schemas not supplied | 2026-08-10 | Confirm before executing deferred positive API cases |
