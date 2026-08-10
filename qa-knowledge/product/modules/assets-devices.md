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

## Reusable Regression Areas

- Settings device types and Device Setup Steps mappings.
- Asset Types, Assets, Stock Levels, and stock-order selectors.
- Devices and Client File assigned device/asset views.
- Service Request grids, details, Generate Asset, checklist, and linked records.
- CP Desktop and Portal reports/exports that consume device, asset, or stock descriptions.
- Duplicate reference options and unchanged identifiers, counts, rates, and links.

## Knowledge Status

| Knowledge Item | Source Status | Source / Evidence | Last Updated | Notes |
|---|---|---|---|---|
| LGX VFII device, asset, and stock labels | Confirmed | Jira SMAR-2617; approved Confluence page 2544926721 v18 | 2026-08-10 | VFII is dual frequency; VFI is F1 frequency. |
| Relationship preservation across confirmed consumers | Confirmed | Approved Confluence page 2544926721 v18 | 2026-08-10 | No duplicate reference options or changed linked values. |
| `SmartHome` versus `Smarthome` title capitalization | Conflict | Jira/Confluence titles versus Jira requirement body and approved cases | 2026-08-10 | Product expectations use `SmartHome`; title alignment remains open. |
| Historical audit/change-log label rendering | Open Question | Not defined by SMAR-2617 evidence | 2026-08-10 | Do not infer a rewrite rule. |
