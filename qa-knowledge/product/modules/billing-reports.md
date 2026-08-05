# Billing and Reports — Product Knowledge

## Platforms

- CP Desktop
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

## Regression Areas

- Billing Service Status dialog and existing End Date workflows.
- Monitoring and other non-Hardware recurring services.
- Billing API persistence, authorization, tenant/client targeting and duplicate prevention.
- Client File Device Information Village Rental labels and unrelated fields.
- EventBridge schedule creation, replacement, cancellation, timing and retry observability.
- Village, Provider and Client Billing Reports, filters, calculations and regeneration.
- Monitoring, SIM, Welfare Check, Establishment Fee and Hardware Purchase report/export behavior.
- QuickBooks item mappings, invoice descriptions, occurrence sequence and duplicate export protection.

## Knowledge Status

| Knowledge Item | Source Status | Source / Evidence | Last Updated | Notes |
|---|---|---|---|---|
| Hardware Rental term, End Date and automatic-Offline lifecycle | Confirmed | Jira SMAR-2467; approved Confluence page 2581889038 v28 | 2026-08-05 | Reusable CP Desktop, API and scheduler behavior |
| Hardware Rental Billing Report and QuickBooks mapping | Confirmed | Jira SMAR-2467; Confluence pages 2581889038 v28 and 2438201345 v6 | 2026-08-05 | Village and Provider/Client report/export paths |
| Exact Billing API and EventBridge field-level contracts | Open Question | Not supplied in reviewed Jira or Confluence evidence | 2026-08-05 | Use implemented contract and developer-supported evidence; do not hardcode unknown fields |
