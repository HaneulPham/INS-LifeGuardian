# SMAR-2633 — Approved Detailed Test-Case Pattern

This is the primary output example for INS LifeGuardian detailed test cases. It captures the style approved through iterative QA and Rovo review. Use the pattern, not the ticket-specific values, for future tickets.

## What this example teaches

- one logical group at a time;
- plain titles beginning with `Verify `;
- complete first-case navigation in actual workflow order;
- exact sample data and calculations;
- Expected Result and Expected Integration grouped by step;
- explicit persistence, no-false-save, idempotency, XML, queue/job, and unchanged-data assertions;
- reviewer feedback classified before cases are changed;
- unconfirmed behaviour deferred instead of guessed.

## Approved full-flow pattern

### Case identity

- **TC ID:** `SMAR-2633-G1-01`
- **Priority:** High
- **Test Area:** `DVA Invoice Generation`
- **Title:** `Verify the first invoice uses the Install Date month when Install Date is later than Presc On`

The title is plain text, starts with `Verify `, and states one calculation rule.

### Preconditions pattern

- A completed DVA Work Order exists.
- Install Date = `12/05/2025`.
- Presc On = `10/05/2025`.
- Next Invoice Due/current invoice period = `01/05/2025`.
- The Work Order contains at least one rental item.
- No invoice has been generated for the Work Order.

Preconditions contain exact scenario data and record state, not ordinary login instructions.

### Test Steps pattern

1. Log in to CP Web.
2. Navigate to **Work Orders → Work Order Management**.
3. Locate the prepared Work Order.
4. Review the Work Order and confirm Install Date, Presc On, and Next Invoice Due match the Preconditions.
5. Generate the first invoice.
6. Open the generated invoice.
7. Review Rental Start Date and Rental Start Period Date.
8. Navigate to **Raptor → DVA Submissions**.
9. Locate and select the generated invoice, then click **Validate Invoices Before Export**.
10. Export the invoice.
11. Open the generated DVA XML and inspect `HireStartDate` and `HirePrdStartDate`.

The flow generates the invoice in Work Order Management before moving to DVA Submissions. It does not begin from the wrong screen or hide setup inside Preconditions.

### Expected Result pattern

**Verify after step #4:**

- Install Date = `12/05/2025`.
- Presc On = `10/05/2025`.
- Next Invoice Due = `01/05/2025`.

**Verify after step #5:**

- Exactly one invoice is generated for the selected Work Order and invoice period.
- No invoice-generation error is displayed.

**Verify after step #7:**

- Rental Start Date = `01/05/2025`.
- The system selects Install Date because it is later than Presc On and normalises it to the first day of May 2025.
- Rental Start Date is not stored as raw Install Date `12/05/2025`.
- Rental Start Date is not stored as raw Presc On `10/05/2025`.
- Rental Start Period Date = `01/05/2025`.

**Verify after step #9:**

- IVL027 passes because Rental Start Period Date equals Rental Start Date.
- `Rental Period Start date is before the Rental Start date.` is not displayed.
- The invoice remains eligible for export.

**Verify after step #11:**

- `HireStartDate` = `01/05/2025`.
- `HirePrdStartDate` = `01/05/2025`.
- XML values match the saved invoice values.

The assertions include positive and explicit negative checks. They do not say only `validation passes` or `XML is correct`.

### Expected Integration pattern

**Verify after step #5:**

- The invoice-generation service persists Rental Start Date = `2025-05-01` and Rental Start Period Date = `2025-05-01`.
- Work Order Install Date, Presc On, and Next Invoice Due remain unchanged.
- Only one invoice record is created for the period.

**Verify after step #9:**

- IVL027 reads the persisted invoice values rather than raw Work Order dates.
- No failed-validation record is created.

**Verify after steps #10–11:**

- Exactly one export request and XML record are created.
- Export does not recalculate or overwrite the invoice dates.
- No duplicate export record is created.
- Invoice amount, rental items, and billing period remain unchanged.

The integration checks name observable service/data outcomes and protect against duplicate processing and unintended mutation.

## Approved boundary-addition pattern

When review identified a missing `Presc On on first day` boundary, the new case used the next unused ID `SMAR-2633-G1-09`; it did not renumber approved G1-01 through G1-08.

Expected assertions included:

- Presc On = `01/06/2026` remains `01/06/2026` after start-of-month normalisation.
- The date is not changed to `31/05/2026`, `02/06/2026`, or another adjacent date.
- Backend does not store an off-by-one value due to timezone conversion.
- XML exports the same persisted date.

## Approved mixed-batch pattern

After the user confirmed that batch validation returns individual results and requires a new valid-only selection:

- Invoice A passes IVL027.
- Invoice B fails with the exact IVL027 message.
- The mixed selection creates no XML or partial background export.
- The user clears the selection and selects only Invoice A.
- Exactly one export is created for Invoice A.
- No export request, XML, queue message, or DVA submission is created for Invoice B.

This is a separate case because batch isolation and no-partial-export are distinct risks from single-invoice validation.

## Approved reviewer-feedback decision pattern

| Feedback | Decision | Reason |
|---|---|---|
| Add Presc On on the first day of the month | Add | Distinct boundary and timezone/off-by-one risk. |
| Add Buy/Recycle regression | Add in regression group | Valid impact coverage but not part of rental calculation Group 1. |
| Add mixed batch pass/fail | Defer, then Add after confirmation | Batch selection existed, but exact valid/invalid export behaviour first required confirmation. |
| Add an exact Rental End Date to the generation case | Defer | The ticket did not define the source or generation formula; guessing would create a false expected result. |

## Weak patterns to reject

- `Title: Invoice generation works correctly`
- `1. Go to Raptor and generate invoice` when generation actually begins in Work Order Management
- `Expected: The dates are correct`
- `Status remains Rejected or becomes Pending`
- `Rental End Date = 31/05/2025` without a confirmed generation rule
- creating separate cases that differ only by wording or another date from the same equivalence class
- changing all approved IDs after adding one boundary case

## Deferred Scenarios pattern

List a scenario here when the expected business outcome is not confirmed. State the missing rule, why it matters, and which group/case would be updated after confirmation. Do not include an executable row with alternative or guessed expected results.
