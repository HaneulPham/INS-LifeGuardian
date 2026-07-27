# INS LifeGuardian Decision Log

This file stores confirmed BA, Product, Dev, and QA decisions that may be reused across INS LifeGuardian tickets.

## Usage Rules

- Record only decisions supported by Jira, Confluence, approved comments, implementation evidence, or confirmed product behaviour.
- Do not record an assumption as a confirmed decision.
- Use only supported Source Status values:
  - Confirmed
  - QA Assumption
  - Open Question
  - Out of Scope
  - Deprecated
  - Conflict
- When a decision changes, do not silently delete the previous decision. Mark it as `Deprecated` or `Conflict` and add the replacement decision.

## Decisions

| Decision ID | Date | Module / Feature | Decision | Source / Evidence | Source Status | Related Tickets | Replaces / Conflicts With | Notes |
|---|---|---|---|---|---|---|---|---|
| DEC-001 | 2026-07-18 | Service Requests | Billing is a manually selectable Service Request Type together with Technical Issue, New Install, and Repair Devices | SMAR-2651 approved QA requirement | Confirmed | SMAR-2651 | N/A | Billing list position is not enforced |
| DEC-002 | 2026-07-20 | Device Setup Steps | Generate CAMS Asset requires and must remain after Assign To Client File; Generate Asset is independent of Generate CAMS Asset | Jira SMAR-2652 and approved Confluence page 2583953435 version 7 | Confirmed | SMAR-2652 | N/A | Deleting Assign To Client File is blocked while Generate CAMS Asset exists and uses the exact Jira validation message |
| DEC-003 | 2026-07-18 | Care Plan Tasks | Simple, Instruction, and Button Log styles support one schedule; Checklist and Grid support multiple schedules | MA-2136 approved QA knowledge | Confirmed | MA-2136 | N/A | Changing from multi-schedule to single-schedule style removes existing schedules |
| DEC-004 | 2026-07-21 | DVA Billing | Generate a rental invoice with Rental Start Date = StartOfMonth(Max(Install Date, Presc On)) and Rental End Date = the last day of that month; XML uses persisted invoice dates; only Pending or Rejected invoices allow rental-date edits; IVL027 fails when Rental Start Period Date is earlier than Rental Start Date | Jira SMAR-2633; approved Confluence page 2566619137 v35; user approval | Confirmed | SMAR-2633 | N/A | Work Order dates remain unchanged; Buy and Recycle invoices remain outside rental-only calculation and IVL027 |
| DEC-005 | 2026-07-25 | Old Backend Authentication / Client Regression | SMAR-2658 client workflow regression covers CP Desktop and Portal Web | User decision Q1-B and exact approval phrase | Confirmed | SMAR-2658 | Jira and Confluence wording named CP Web and Portal Web | This user-confirmed active-ticket decision replaces CP Web with CP Desktop for Group 6. |
| DEC-006 | 2026-07-25 | Old Backend Authentication / Error Contract | SMAR-2658 authentication failures use the existing Old Backend response envelope and contract; QA must not hardcode `401 Unauthorized` without verified implementation evidence | User decision Q2-B; API Responses (Old BE) page 2123300865 v2; exact approval phrase | Confirmed | SMAR-2658 | Approved Confluence v22 cases that assumed `401 Unauthorized` | Exact implemented numeric status and payload fields remain Open Questions. |
| DEC-007 | 2026-07-27 | Service Requests / Asset Type Mapping | Generate Asset from Service Requests maps SafetyWatch stock to SafetyWatch 3 (`SF3`) and SmartTracker stock to SmartTracker 3 (`ST3`); manual Asset Management retains explicit legacy/v3 selection and existing legacy Service Request assets remain unchanged | Jira SMAR-2659 description and comments 44179/44299; approved Confluence page 2589687817 v13; exact approval phrase | Confirmed | SMAR-2659 | N/A | Exact backend routes and conditional billing/report observability remain Open Questions. |
