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

## Confirmed QuickBooks Invoice Description Rules

- Provider and Client invoice descriptions do not include Client File name, Village name, Date On, or Date Off.
- Monitoring uses `{DEVICE_TYPE} - Alarm Rental and Monitoring - {CYCLE} in {TIMING}`.
- Telstra and Voda SIM use `{DEVICE_TYPE} - {CYCLE} in {TIMING}` with the carrier-specific Activity.
- Welfare Check uses `{CYCLE} in {TIMING}`.
- Provider/Client Establishment Fee uses a blank Description and Activity `ESTAB FEE`.
- Provider/Client Hardware Purchase uses `{DEVICE_TYPE}`.
- Recurring Provider/Client mappings cover Monthly, Quarterly, Biannual, and Annual in Advance and Arrears.
- Village Monitoring, SIM, Welfare Check, Establishment Fee, and Hardware Purchase mappings remain regression coverage.
- Hardware Rental term/payment formatting remains governed by the confirmed SMAR-2467 rule. SMAR-2576 case page 2534605201 v8 omits that suffix and is Conflict evidence, not a replacement rule.

## Confirmed DVA Prior Approval Number Rules

- Work Orders and Invoices reject normalized exact `N/A`, `NA`, and `None` Prior Approval Number values case-insensitively in CP Web and the API.
- A supplied whitespace-only value is invalid, while a genuinely empty optional value remains allowed.
- Leading and trailing whitespace is trimmed before persistence; internal characters and variable valid free-text formats remain unchanged.
- Invalid API input returns HTTP `400 Bad Request` with `Error = "bad_request"` and `ErrorDescription = "'Dva Presc On' must be a valid value or blank"`.
- Historical invalid values remain viewable but must be corrected or cleared before an affected Work Order or Invoice update can persist.
- Final CP Web invalid-input presentation and exact message remain unresolved because current Jira and approved Confluence evidence conflict.

## Confirmed DVA Invoice Pre-Export Validation Rules

- In CP Web Raptor DVA Submissions, **Validate Invoices Before Export** rejects selected invoices whose Prior Approval Number is exactly `N/A`, `N.A`, `NA`, or whitespace only.
- The affected selected row's **Errors** column displays `Prior App Number must be blank or a valid number.`
- A genuinely blank Prior Approval Number does not trigger this error and remains eligible for the next export step when no other validation errors exist.
- Validation applies only to selected invoices and does not change invoice status or automatically modify the stored Prior Approval Number.
- After correction to valid value `123456`, the saved value remains after reopen and the selected invoice displays `The invoice has no validation errors.` when no other errors exist.
- Lowercase/alternate-separator normalization and `None` handling at this pre-export stage remain Open Questions; do not infer them from the distinct SMAR-2528 save-time rule.

## Confirmed DVA Mandatory Work Order and Invoice Fields

- CP Web Add Work Order, Edit Work Order, and Edit Invoice enforce requiredness for Client First Name, Client Last Name, Client/Invoice Postcode, Client/Invoice Address, Delivery Postcode, and Delivery Address.
- A blank applicable mandatory value prevents Save/Next from reaching a completed persisted create or update state.
- After the applicable missing value is populated, the record can be saved and the value remains after reopen.
- SMAR-2600 does not add postcode numeric-format or valid-State validation.
- Exact validation text, simultaneous multi-field presentation, checked Same As Client Details behavior, historical incomplete-record handling, Client File synchronization, and backend/API enforcement remain unconfirmed.

## Regression Areas

- Billing Service Status dialog and existing End Date workflows.
- Monitoring and other non-Hardware recurring services.
- Billing API persistence, authorization, tenant/client targeting and duplicate prevention.
- Client File Device Information Village Rental labels and unrelated fields.
- EventBridge schedule creation, replacement, cancellation, timing and retry observability.
- Village, Provider and Client Billing Reports, filters, calculations and regeneration.
- Monitoring, SIM, Welfare Check, Establishment Fee and Hardware Purchase report/export behavior.
- QuickBooks item mappings, invoice descriptions, occurrence sequence and duplicate export protection.
- Provider/Client removal of legacy Client File/Village/date text, service-specific Cycle/Timing templates, blank Establishment Fee behavior, carrier Activity, and billing-party isolation.
- Work Order create/update and Invoice update optional-value, exact-match, case-insensitive, whitespace, free-text, atomic-rejection, and historical-correction behavior.
- CP Web/API convergence for persisted Prior Approval Number values and protection of Invoice status, totals, payment state, and export state.
- Raptor DVA selected-record validation for exact invalid Prior Approval values, whitespace-versus-blank handling, Errors-column messaging, non-mutation, and correction/revalidation before export.
- SMAR-2633 DVA rental-date generation and XML export using supported Presc On data.

## Knowledge Status

| Knowledge Item | Source Status | Source / Evidence | Last Updated | Notes |
|---|---|---|---|---|
| Hardware Rental term, End Date and automatic-Offline lifecycle | Confirmed | Jira SMAR-2467; approved Confluence page 2581889038 v28 | 2026-08-05 | Reusable CP Desktop, API and scheduler behavior |
| Hardware Rental Billing Report and QuickBooks mapping | Confirmed | Jira SMAR-2467; Confluence pages 2581889038 v28 and 2438201345 v6 | 2026-08-05 | Village and Provider/Client report/export paths |
| Provider/Client non-Hardware-Rental QuickBooks description templates and Village regression | Confirmed | Jira SMAR-2576; Confluence pages 2438201345 v6 and 2534605201 v8 | 2026-08-13 | Monitoring, Telstra/Voda SIM, Welfare Check, Establishment Fee, and Hardware Purchase |
| SMAR-2576 Hardware Rental rows without term/payment suffix | Conflict | Confluence page 2534605201 v8 conflicts with linked page 2438201345 v6 and DEC-015/SMAR-2467 | 2026-08-13 | Ten source rows deferred; do not replace confirmed Hardware Rental knowledge without a new decision |
| Exact Billing API and EventBridge field-level contracts | Open Question | Not supplied in reviewed Jira or Confluence evidence | 2026-08-05 | Use implemented contract and developer-supported evidence; do not hardcode unknown fields |
| DVA Prior Approval Number invalid list, whitespace distinction, trimming, affected records, and API 400 contract | Confirmed | Jira SMAR-2528 current description; Confluence page 2628780034 v10 | 2026-08-10 | Reusable Work Order and Invoice validation behavior |
| CP Web invalid-input presentation and exact message for Prior Approval Number | Conflict | Jira SMAR-2528 description and comment 44529; Confluence page 2628780034 v10 | 2026-08-10 | Resolve error display versus field clearing and `Presc On.` versus `Dva Presc On` wording before activating deferred UI cases |
| Work Order/Invoice route methods and successful API response contracts for SMAR-2528 | Open Question | Confluence assumptions A1–A3; successful response schemas not supplied | 2026-08-10 | Confirm before executing deferred positive API cases |
| Raptor DVA selected-invoice Prior Approval validation, exact message, blank handling, isolation, and non-mutation | Confirmed | Jira SMAR-2504; Confluence page 2564390934 v7 | 2026-08-13 | Distinct pre-export workflow; 5 normalized cases stored |
| Raptor DVA lowercase/alternate-separator normalization and `None` handling | Open Question | SMAR-2504 does not define these outcomes; related SMAR-2528 applies at save time | 2026-08-13 | Do not promote cross-stage behavior without confirmation |
| DVA Work Order/Invoice mandatory identity and address fields | Confirmed | Jira SMAR-2600; Confluence page 2644836353 v3 | 2026-08-13 | CP Web create/edit validation; requiredness only |
| SMAR-2600 validation presentation, historical data, Client File isolation, Same As behavior, and backend contract | Open Question | Confluence page 2644836353 v3 contains assumptions not confirmed by Jira | 2026-08-13 | 14 executable cases stored and 13 source cases deferred |
