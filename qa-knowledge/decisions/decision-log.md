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
