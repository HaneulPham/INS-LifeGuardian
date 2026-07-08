# SMAR-2504 - CP Web Raptor DVA Prior Approval Number Validation

Supporting QA memory for SMAR-2504. Current Jira requirements, confirmed BA
decisions, verified API contracts, and current product behavior take precedence.

## Source Evidence

- Ticket: SMAR-2504 - CP Web - Validate "N/A" for Prior Approval Number.
- User-supplied path: CP Web -> Work Orders -> Invoice Management -> Raptor DVA Submissions.
- User-supplied test case group: CP Web -> Raptor DVA Submissions -> Validate Selected Records.
- Review date: 2026-07-08.

## Confirmed Requirement

- Validation runs only when the user clicks **Validate Invoices Before Export**.
- Validation applies to selected records only.
- Invalid Prior Approval Number values must display the message
  **Prior App Number must be blank or a valid number.** in the **Errors** column.
- One selected invoice with an invalid Prior Approval Number blocks the entire export validation result.
- Invoice status is not updated by this validation.
- **Export** is not required to run this new validation rule independently.
- Prior Approval Number is editable only from CP Web.
- There is no separate strict numeric-format rule for Prior Approval Number.

## Confirmed Invalid Values

- `N/A`
- `NA`
- Whitespace-only value

## QA Assumptions / Needs Confirmation

- Case-insensitive variants such as `n/a`, `na`, `N/a`, and `Na` should be treated as the same INS placeholder rule. Needs confirmation if not explicitly approved by BA.
- Separator variants such as `N / A`, `N-A`, and `N.A` should be treated as the same INS placeholder rule. Needs confirmation if not explicitly approved by BA.
- Leading/trailing spaces around invalid values such as ` N/A ` should fail validation if comparison is performed against the meaningful value. Needs confirmation because the user said trimming is not required.
- If success text appears in **Errors** column, the exact text **The invoice has no validation errors.** must be verified in product before treating it as a confirmed expected result.
- Unknown backend endpoint, request payload, response schema, and error field names remain `Needs confirmation`.

## Recommended Test Groups

1. **Validation Trigger and Scope**
   - Validate rule runs from **Validate Invoices Before Export** only.
   - Validate selected records only.
   - Validate unselected invalid records do not affect selected-record validation.

2. **Invalid Prior Approval Number Values**
   - `N/A`
   - `NA`
   - Whitespace-only value
   - QA assumption variants: `n/a`, `na`, `N / A`, `N-A`, `N.A`

3. **Allowed Prior Approval Number Values**
   - Blank Prior Approval Number.
   - Non-banned value such as `123456` or an existing production-style value.
   - Avoid calling this strict "valid number" coverage unless a numeric-format rule is later confirmed.

4. **Errors Column Display**
   - Error appears in the correct selected invoice row.
   - Error text is exactly **Prior App Number must be blank or a valid number.**
   - Existing validation errors are not incorrectly hidden. Append/replace behavior is `Needs confirmation`.

5. **Export Blocking and Data Integrity**
   - One invalid selected invoice blocks the entire export validation result.
   - Validation does not create an export file/submission.
   - Validation does not change invoice status.
   - Validation does not auto-clear, trim, or reformat Prior Approval Number.

6. **Correction and Revalidation**
   - After editing an invalid Prior Approval Number to a non-banned value and saving, selected invoice validates without the SMAR-2504 error.
   - Previous **Prior App Number must be blank or a valid number.** error is cleared after correction and re-validation.
   - Repeated validation clicks do not duplicate stale Prior Approval Number error messages.

7. **Regression**
   - Existing Raptor DVA validation rules still run.
   - Valid selected invoices can still pass pre-export validation.
   - Filters/search/current-page selection do not cause validation to run against the wrong invoices.

## Reviewed Test Cases

- TC-SMAR2504-WEB-001: selected invoice with Prior Approval Number = `N/A` fails validation.
- TC-SMAR2504-WEB-002: selected invoice with Prior Approval Number = `NA` fails validation.
- TC-SMAR2504-WEB-003: selected invoice with whitespace-only Prior Approval Number fails validation.
- TC-SMAR2504-WEB-004: selected invoice with blank Prior Approval Number passes SMAR-2504 validation.
- TC-SMAR2504-WEB-005: selected invoice with non-banned Prior Approval Number does not fail SMAR-2504 validation.
- TC-SMAR2504-WEB-006: validation applies only to selected records.
- TC-SMAR2504-WEB-007: INS placeholder variants are rejected when confirmed as part of the same INS rule.
- TC-SMAR2504-WEB-008: correction path for editing Prior Approval Number, saving, reopening, selecting invoice, and validating.

## Full Web Test Cases

**QA Assumptions**

- Validation runs only when user clicks **Validate Invoices Before Export**.
- Validation applies to selected records only.
- Error displays in **Errors** column.
- Invoice status is not updated by this validation.
- No strict numeric format validation exists except blocking INS placeholder values.
- Success message **The invoice has no validation errors.** is `Needs confirmation` unless already verified in product.

| TC ID | Priority | Feature | Test Area | Title | Preconditions | Test Steps | Expected Result | Expected Integration | Browser/Device | Accessibility Check | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC-SMAR2504-WEB-001 | High | Raptor DVA Submissions | CP Web -> Work Orders -> Invoice Management -> Raptor DVA Submissions | Verify selected invoice with Prior Approval Number = `N/A` fails validation | • Raptor DVA invoice exists with Prior Approval Number = `N/A`.<br>• Invoice is visible in Raptor DVA Submissions grid.<br>• User has permission to validate invoices. | 1. Open CP Web.<br>2. Go to **Work Orders -> Invoice Management -> Raptor DVA Submissions**.<br>3. Select the invoice where Prior Approval Number = `N/A`.<br>4. Click **Validate Invoices Before Export**.<br>5. Review the selected invoice row. | **Verify after step #4-5:**<br>• Validation does not pass for the selected invoice.<br>• **Errors** column displays: `Prior App Number must be blank or a valid number.`<br>• Invoice status is not changed by this validation.<br>• Prior Approval Number value remains `N/A`; system does not auto-clear or modify it. | **Verify after step #4-5:**<br>• CP Web sends validation request for the selected invoice only.<br>• Backend returns validation failure for Prior Approval Number.<br>• No export file/submission is generated by this validation action.<br>• No invoice status update is triggered. | Chrome / Edge on desktop | • Error text is readable without relying only on color.<br>• Keyboard user can select row and trigger validation. | Core invalid value from requirement. |
| TC-SMAR2504-WEB-002 | High | Raptor DVA Submissions | CP Web -> Work Orders -> Invoice Management -> Raptor DVA Submissions | Verify selected invoice with Prior Approval Number = `NA` fails validation | • Raptor DVA invoice exists with Prior Approval Number = `NA`.<br>• Invoice is visible in grid. | 1. Open **Raptor DVA Submissions**.<br>2. Select the invoice where Prior Approval Number = `NA`.<br>3. Click **Validate Invoices Before Export**.<br>4. Review the **Errors** column. | **Verify after step #3-4:**<br>• Selected invoice fails validation.<br>• **Errors** column displays: `Prior App Number must be blank or a valid number.`<br>• Prior Approval Number remains `NA` after validation.<br>• Invoice status remains unchanged. | **Verify after step #3-4:**<br>• Validation request includes the selected invoice.<br>• Backend applies INS custom rule and returns row-level error.<br>• No export/submission is created. | Chrome / Edge on desktop | • Error message remains visible after grid focus changes. | Core invalid value from requirement. |
| TC-SMAR2504-WEB-003 | High | Raptor DVA Submissions | CP Web -> Work Orders -> Invoice Management -> Raptor DVA Submissions | Verify selected invoice with whitespace-only Prior Approval Number fails validation | • Raptor DVA invoice exists with Prior Approval Number containing whitespace only, e.g. `" "`.<br>• Invoice is visible in grid. | 1. Open **Raptor DVA Submissions**.<br>2. Select the invoice where Prior Approval Number is whitespace only.<br>3. Click **Validate Invoices Before Export**.<br>4. Review the selected invoice row. | **Verify after step #3-4:**<br>• Selected invoice fails validation.<br>• **Errors** column displays: `Prior App Number must be blank or a valid number.`<br>• Whitespace-only value is not treated as blank.<br>• Invoice status remains unchanged. | **Verify after step #3-4:**<br>• Backend identifies whitespace-only value as invalid.<br>• Validation failure is returned for the selected invoice.<br>• No data update or export is triggered. | Chrome / Edge on desktop | • Error message is accessible when horizontal scrolling is required to view **Errors** column. | Confirms whitespace-only rule. |
| TC-SMAR2504-WEB-004 | Medium | Raptor DVA Submissions | CP Web -> Work Orders -> Invoice Management -> Raptor DVA Submissions | Verify selected invoice with blank Prior Approval Number passes validation | • Raptor DVA invoice exists with Prior Approval Number blank/empty.<br>• No other validation errors exist for this invoice. | 1. Open **Raptor DVA Submissions**.<br>2. Select the invoice where Prior Approval Number is blank.<br>3. Click **Validate Invoices Before Export**.<br>4. Review the **Errors** column for the selected invoice. | **Verify after step #3-4:**<br>• Selected invoice does not show Prior Approval Number validation error.<br>• **Errors** column does not display `Prior App Number must be blank or a valid number.`<br>• Invoice remains eligible for the next export process if no other validation errors exist.<br>• Invoice status remains unchanged. | **Verify after step #3-4:**<br>• Backend accepts blank Prior Approval Number.<br>• No Prior Approval Number validation error is returned.<br>• No export is generated by validation action. | Chrome / Edge on desktop | • Blank value does not create misleading visual error state. | Confirms blank is valid. |
| TC-SMAR2504-WEB-005 | Medium | Raptor DVA Submissions | CP Web -> Work Orders -> Invoice Management -> Raptor DVA Submissions | Verify selected invoice with non-banned Prior Approval Number value does not fail SMAR-2504 validation | • Raptor DVA invoice exists with Prior Approval Number using a non-banned value, e.g. `123456` or existing valid business value.<br>• No other validation errors exist for this invoice. | 1. Open **Raptor DVA Submissions**.<br>2. Select the invoice with non-banned Prior Approval Number.<br>3. Click **Validate Invoices Before Export**.<br>4. Review the **Errors** column. | **Verify after step #3-4:**<br>• Selected invoice does not show the SMAR-2504 Prior Approval Number error.<br>• Value is not rejected only because it is not strictly numeric, unless another existing validation rule rejects it.<br>• Invoice status remains unchanged. | **Verify after step #3-4:**<br>• Backend does not apply extra numeric-format validation for SMAR-2504.<br>• Validation response does not include Prior Approval Number error for non-banned values. | Chrome / Edge on desktop | • User can identify validation result clearly from grid row. | Requirement confirms no exact valid-number rule. |
| TC-SMAR2504-WEB-006 | High | Raptor DVA Submissions | CP Web -> Work Orders -> Invoice Management -> Raptor DVA Submissions | Verify validation applies only to selected records | • Invoice A has Prior Approval Number = blank or valid value.<br>• Invoice B has Prior Approval Number = `N/A`.<br>• Both invoices are visible in grid.<br>• Invoice B is not selected. | 1. Open **Raptor DVA Submissions**.<br>2. Select Invoice A only.<br>3. Leave Invoice B unselected.<br>4. Click **Validate Invoices Before Export**.<br>5. Review validation result for both rows.<br>6. Select Invoice B.<br>7. Click **Validate Invoices Before Export** again. | **Verify after step #4-5:**<br>• Validation is performed for Invoice A only.<br>• Invoice B does not block validation while unselected.<br>• Invoice B does not receive a new **Errors** column update from this action.<br><br>**Verify after step #7:**<br>• Invoice B fails validation.<br>• Invoice B **Errors** column displays: `Prior App Number must be blank or a valid number.` | **Verify after step #4-5:**<br>• Validation API receives only selected invoice IDs/records.<br>• Unselected invoice records are not included in validation payload.<br>• No export/submission is generated.<br><br>**Verify after step #7:**<br>• Validation API receives Invoice B after it is selected.<br>• Backend returns Prior Approval Number validation error for Invoice B. | Chrome / Edge on desktop | • Checkbox selection state is visually clear and keyboard accessible. | Important selected-record scope test. |
| TC-SMAR2504-WEB-007 | Medium | Raptor DVA Submissions | CP Web -> Work Orders -> Invoice Management -> Raptor DVA Submissions | Verify INS placeholder variants are rejected for selected records | • Test invoices exist with Prior Approval Number values such as `n/a`, `na`, `N / A`, `N-A`, or `N.A` if supported by setup.<br>• Invoices are visible in grid. | 1. Open **Raptor DVA Submissions**.<br>2. Select invoice records with INS placeholder variant values.<br>3. Click **Validate Invoices Before Export**.<br>4. Review the **Errors** column for each selected invoice. | **Verify after step #3-4:**<br>• Each selected invoice using an INS placeholder variant fails validation if defined as part of the same INS rule.<br>• **Errors** column displays: `Prior App Number must be blank or a valid number.` for failed rows.<br>• Invoice statuses remain unchanged. | **Verify after step #3-4:**<br>• Backend applies the INS placeholder validation consistently across selected records.<br>• Row-level errors are returned for each invalid selected invoice.<br>• No data is auto-corrected. | Chrome / Edge on desktop | • Multiple row errors remain readable and associated with the correct row. | Dependent on final confirmation that these variants are included in the same INS rule. |
| TC-SMAR2504-WEB-008 | High | Raptor DVA Submissions | CP Web -> Prior Approval Number Edit Source | Verify updating invoice with non-banned Prior Approval Number validates successfully | • Raptor DVA invoice exists with editable Prior Approval Number.<br>• Invoice is visible in **Raptor DVA Submissions**.<br>• User has permission to edit Prior Approval Number and validate invoices.<br>• Invoice has no other validation errors. | 1. Open the CP Web source screen where Prior Approval Number is editable.<br>2. Update Prior Approval Number to a non-banned value, e.g. `123456`.<br>3. Save the invoice.<br>4. Reopen the invoice and confirm Prior Approval Number is saved as `123456`.<br>5. Go to **Work Orders -> Invoice Management -> Raptor DVA Submissions**.<br>6. Select the updated invoice.<br>7. Click **Validate Invoices Before Export**.<br>8. Review the **Errors** column for the selected invoice. | **Verify after step #3-4:**<br>• Prior Approval Number is saved successfully.<br>• Reopened invoice shows the updated value `123456`.<br><br>**Verify after step #7-8:**<br>• Selected invoice validates successfully for SMAR-2504 rule.<br>• **Errors** column does not display: `Prior App Number must be blank or a valid number.`<br>• No previous `Prior App Number must be blank or a valid number.` error remains after the corrected value is saved and validated.<br>• If configured and verified, **Errors** column displays: **The invoice has no validation errors.** `Needs confirmation`.<br>• Invoice status is not changed by this validation action. | **Verify after step #3:**<br>• CP Web save API persists the updated Prior Approval Number.<br><br>**Verify after step #7-8:**<br>• Raptor DVA validation uses the latest saved value.<br>• Backend returns successful validation result for the selected invoice. `Needs confirmation` if API/log evidence is unavailable.<br>• No export file/submission is generated by the validation action. | Chrome / Edge on desktop | • Success or no-error state in **Errors** column is readable and associated with the correct selected row.<br>• User can reach the row checkbox and validation button using keyboard. | Happy-path correction case after invalid `N/A`, `NA`, or whitespace-only values are fixed. |

## TC-008 Review Notes

- Keep TC-008 as the happy-path correction case after invalid `N/A`, `NA`, or whitespace-only values are fixed.
- Preferred title wording: **Verify updating invoice with non-banned Prior Approval Number validates successfully**.
- Avoid implying a strict numeric-format rule unless BA/API later confirms one.
- If **The invoice has no validation errors.** appears in **Errors** column, treat it as confirmed only after product verification.
- Minimal useful expected-result addition:
  - No previous **Prior App Number must be blank or a valid number.** error remains after the corrected value is saved and validated.
- The longer expanded expected-result wording was reviewed but intentionally not adopted because the user said it is not needed.

## Risk Notes

- Main regression risk is stale validation state: user corrects Prior Approval Number, but the grid still displays the old error.
- Main scope risk is validating unselected rows or current-page/filter rows instead of selected records only.
- Main implementation risk is adding strict numeric validation even though no numeric-format rule is confirmed.
- Backend/API enforcement is still `Needs confirmation`; UI-only validation could be bypassed by direct calls if backend does not enforce the rule.
