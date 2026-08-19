# Assets and Devices — Product Knowledge

## Platforms

- CP Desktop
- Portal Web
- Backend APIs
- Twilio incoming-message alarm path

## Confirmed SafetyWatch LineNumber Mapping

- A returned SafetyWatch uses its stored LineNumber when populated.
- When stored SafetyWatch LineNumber is blank, returned/transformed LineNumber remains blank and does not use the system-generated Asset Barcode.
- SmartHomeMini/Mobile retains the existing Asset Barcode fallback when its LineNumber is blank.
- CP Device Listing/DeviceTransformer must show the same device-type-specific mapping without persisting a response fallback into device data.
- `GetDeviceByLineNumberRequest` can resolve a SafetyWatch through its unique stored LineNumber for the existing Twilio incoming-message alarm path.
- Whether a blank-LineNumber SafetyWatch may be found directly through its Asset Barcode is Conflict evidence in SMAR-2404 and must not be treated as reusable confirmed behavior.

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

## Confirmed InteliCare Dialler Rules

- `InteliCare Dialler` is a distinct CP Asset Type, Device Type, Stock Type, billing identity, and report identity while using the approved LGX/CAMS runtime behavior.
- Generated assets use exact ten-character `IN########` barcodes beginning at `IN00000001` when `LastBarcodeId = 0`; generated devices use an `I`-prefixed Device Code.
- InteliCare supports the approved Asset Management, Stock, Settings, Device Setup, Devices, Service Request/CAMS creation, Client File assignment, alarm, SIP/DTMF, SMS/command, power/battery, peripheral, SIM/Jasper, and lifecycle workflows.
- Existing LGX and other device records are not automatically migrated or reclassified; only a targeted authorized workflow changes a record.
- Compatible code containing the compiled InteliCare enum must be deployed before the RavenDB `AssetType` document is created.
- For SMAR-2700, Return Received moves quantity from Pending Return to In Stock while leaving Total and Available unchanged when Allocated is unchanged; this ticket-specific decision does not replace DEC-021 as a universal Stock rule.

## Reusable Regression Areas

- Settings device types and Device Setup Steps mappings.
- Asset Types, Assets, Stock Levels, and stock-order selectors.
- Stock Levels formulas, manual Stock actions, Stock Transaction History, Stock/StockTrans API compatibility, and Service Request allocation/dispatch/reversal.
- Devices and Client File assigned device/asset views.
- Service Request grids, details, Generate Asset, checklist, and linked records.
- Peripheral Select/Create/Listen eligibility, parent-versus-top-level Client File source, CAMS/INS device placement, alarm matching, duplicate prevention, and asymmetric removal.
- CP Desktop and Portal reports/exports that consume device, asset, or stock descriptions.
- Duplicate reference options and unchanged identifiers, counts, rates, and links.
- InteliCare-versus-LGX catalogue, identifier, Stock, Service Request, CAMS/runtime, SIM/Jasper, Client File, and lifecycle isolation.
- SafetyWatch versus SmartHomeMini/Mobile LineNumber/Barcode mapping across dispatcher responses, DeviceTransformer, CP Device Listing, Client File device loading, billing consumers, and Twilio lookup.
- Unique LineNumber/Barcode test data and DeviceUuid/client-file verification to prevent wrong-device or cross-client alarm association.

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
| InteliCare Dialler identity, identifiers, LGX/CAMS parity, lifecycle, and Service Request support | Confirmed | Jira SMAR-2700; Confluence page 2658795521 v17; DEC-033 | 2026-08-19 | 108 normalized cases across seven groups; exact low-level contracts require supported evidence where needed |
| SafetyWatch returned LineNumber and SmartHomeMini/Mobile fallback mapping | Confirmed | Jira SMAR-2404 description/Test Cases; Jira SMAR-2403; Confluence page 2644410373 v3 | 2026-08-19 | 17 normalized cases stored; direct SafetyWatch-by-Barcode lookup remains Conflict. |
| Blank-LineNumber SafetyWatch lookup through Asset Barcode | Conflict | Jira SMAR-2404 Test Cases versus Confluence page 2644410373 v3 G1-06/G2-02 | 2026-08-19 | Do not activate the direct lookup or derived Twilio case until clarified. |
| Exact dispatcher accepted/not-found and Twilio unresolved-device contracts | Open Question | Not defined by reviewed SMAR-2404/SMAR-2403 evidence | 2026-08-19 | Record deployed status/body and use sanitized correlation evidence. |
