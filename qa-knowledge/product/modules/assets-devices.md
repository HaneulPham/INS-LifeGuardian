# Assets and Devices — Product Knowledge

## Platforms

- CP Desktop
- Portal Web

## Confirmed LGX VFII Reference Labels

- The dual-frequency device type current label is `SmartHome LGX VFII`.
- The dual-frequency asset type current label is `SmartHome LGX VFII`.
- The related stock type current label is `SmartHome LGX VFII Dialler`.
- VFI refers to the F1-frequency model and is not interchangeable with VFII.
- Reference-description changes must preserve existing device, asset, stock, client-file, Service Request, setup-step, and billing relationships.

## Confirmed Asset Import Identifier Updates

- CP Desktop Import Asset accepts the mandatory `Barcode,Imei,MacAddress` CSV format.
- Barcode plus the selected Asset Type targets an existing asset; a mismatched selected Asset Type is a validation failure.
- An existing match is updated in place and only supplied Imei/MacAddress values change; blank optional values do not clear stored values.
- An unmatched Barcode continues through the existing new-asset creation path.
- Supplied Imei is 15 numeric digits and Luhn-valid; supplied MacAddress contains six colon-separated hexadecimal pairs.
- Leading/trailing whitespace is removed before matching, validation, blank evaluation, and persistence.
- Duplicate Barcode behavior within one CSV and exact backend/audit contracts remain open.

## Confirmed Peripheral Service Request Steps

- The 18 SMAR-2537 supported non-PIR peripherals use Custom, Select Client File, Create Medi Alarm, and Listen for Alarm when top-level; a child instance omits Select Client File and uses the parent Assign to Client File context.
- PIR uses Custom, Select Client File, and Create Medi Alarm when top-level, omits Select Client File when a child, and does not use Listen for Alarm.
- Other peripheral types remain Custom-only.
- Create Medi Alarm persists one CAMS or INS device against the topology-specific File and Client and places it in the corresponding Client File device category.
- Listen for Alarm must match the intended File, topology/main-parent context, and generated Medi Alarm UUID; the legacy `RecivedFromMediAlarmDeviceId` field stores that UUID for mobile backward compatibility.
- Service Request-initiated removal deletes the generated device from the Client File; direct Client File deletion does not rewrite the originating Service Request.

## Reusable Regression Areas

- Settings device types and Device Setup Steps mappings.
- Asset Types, Assets, Stock Levels, and stock-order selectors.
- Stock Levels formulas, manual Stock actions, Stock Transaction History, Stock/StockTrans API compatibility, and Service Request allocation/dispatch/reversal.
- Devices and Client File assigned device/asset views.
- Service Request grids, details, Generate Asset, checklist, and linked records.
- Peripheral Select/Create/Listen eligibility, parent-versus-top-level Client File source, CAMS/INS device placement, alarm matching, duplicate prevention, and asymmetric removal.
- CP Desktop and Portal reports/exports that consume device, asset, or stock descriptions.
- Duplicate reference options and unchanged identifiers, counts, rates, and links.

## Knowledge Status

| Knowledge Item | Source Status | Source / Evidence | Last Updated | Notes |
|---|---|---|---|---|
| LGX VFII device, asset, and stock labels | Confirmed | Jira SMAR-2617; approved Confluence page 2544926721 v18 | 2026-08-10 | VFII is dual frequency; VFI is F1 frequency. |
| Relationship preservation across confirmed consumers | Confirmed | Approved Confluence page 2544926721 v18 | 2026-08-10 | No duplicate reference options or changed linked values. |
| `SmartHome` versus `Smarthome` title capitalization | Conflict | Jira/Confluence titles versus Jira requirement body and approved cases | 2026-08-10 | Product expectations use `SmartHome`; title alignment remains open. |
| Historical audit/change-log label rendering | Open Question | Not defined by SMAR-2617 evidence | 2026-08-10 | Do not infer a rewrite rule. |
| Stock Total/Qty equals In Stock plus Pending Return; Available equals Total minus Allocated | Confirmed | Stock API Confluence page 1979449346; SMAR-1839 | 2026-08-10 | On Order is stored independently |
| Undefined StockTrans and Service Request stock effects use deployed pre-refactor behavior as their regression baseline | Confirmed | DEC-021; SMAR-1839 user decisions Q1-A, Q2-D, Q3-A | 2026-08-10 | This confirms the evidence source; exact unresolved values remain Open Questions |
| Peripheral eligibility, topology-specific Client File source, Create/Listen workflow, and asymmetric removal | Confirmed | Jira SMAR-2537; Confluence page 2517598218 v49 | 2026-08-13 | 72 reviewed cases are stored; exact API/error/log contracts remain open |
| Active-listener removal, timeout/cancel, and failure-atomicity outcomes | QA Assumption | SMAR-2537 A1–A3 and risk cases | 2026-08-13 | Retain as traceable coverage until baseline or instrumentation evidence confirms exact behaviour |
| Asset Import Barcode/Asset Type matching and Imei/MacAddress update rules | Confirmed | Jira SMAR-2525; Confluence page 2566684674 v11 | 2026-08-13 | 29 normalized cases; duplicate-row behavior and exact backend/audit contracts remain open. |
