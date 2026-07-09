# SMAR-2633 - Export HireStartDate as PrescOn if Less Than RentalStartAt

## Source Evidence

- User-provided Jira ticket screenshot and discussion.
- Module: Billing / DVA Invoice Export.
- Path: CP Web -> Raptor DVA Submissions -> Export Invoice XML.
- Environment from ticket: CP Web - Prod.

## Confirmed Requirement

For DVA rental invoice XML export only:

```text
HireStartDate = RentalStartAt date < PrescOn date ? PrescOn date : RentalStartAt date
DateLastPresc = PrescOn date
```

## Confirmed Scope

- Applies only to Export Invoice XML.
- Applies only to DVA rental items.
- Applies to all DVA rental invoices, not only invoices linked to a new Prior Approval.
- Applies when exporting one invoice and when exporting multiple selected invoices.
- Comparison is date-only, not full datetime.
- PrescOn is required and cannot be blank/null.
- Work Order creation must allow Rental Start Date earlier than, equal to, or later than PrescOn.
- Invoice UI/database/source Rental Start Date must remain unchanged.
- DVA purchase items are not affected by the rental HireStartDate adjustment rule.
- Validation, Errors column, and IVL027 are out of scope for this ticket.
- Exact exported XML date format does not need special coverage beyond existing DVA export behavior.

## Needs Confirmation

- Exact backend/API field name for Rental Start Date.
- Exact backend/API field name for PrescOn.
- Exact backend/API item type field that identifies rental versus purchase.

## Test Case Summary

| Group | Product Path | Purpose |
| --- | --- | --- |
| Group 0 | CP Web -> Work Order -> Invoice Setup | Confirm Work Order creation allows all three Rental Start Date versus PrescOn relationships. |
| Group 1 | CP Web -> Raptor DVA Submissions -> Export Invoice XML | Confirm XML HireStartDate calculation for earlier/equal/later rental date scenarios. |
| Group 2 | CP Web -> Raptor DVA Submissions -> Batch Export Invoice XML | Confirm multiple selected invoices calculate independently. |
| Group 3 | CP Web -> Invoice Source Detail -> Export XML Does Not Persist Adjustment | Confirm export-only transformation does not change source data. |
| Group 4 | CP Web -> Raptor DVA Submissions -> Purchase Item Regression | Confirm purchase items do not use rental HireStartDate adjustment. |
| Group 5 | CP Web -> Raptor DVA Submissions -> Date-Only Comparison | Confirm same calendar date is treated as equal when hidden time differs, if test data allows. |

## Group 0 - CP Web -> Work Order -> Invoice Setup

Scope: Work Order creation/setup only. Export XML value is checked in later groups.

| TC ID | Priority | Feature | Test Area | Title | Preconditions | Test Steps | Expected Result | Expected Integration | Browser/Device | Accessibility Check | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC-SMAR2633-WEB-000 | High | DVA Invoice Export | CP Web -> Work Order -> Invoice Setup | Verify Work Order creation allows Rental Start Date earlier than, equal to, and later than PrescOn | • User can create completed Work Orders with rental items<br>• PrescOn is available and required | 1. Create Work Order A with Rental Start Date = 01/06/2026 and PrescOn = 03/06/2026.<br>2. Create Work Order B with Rental Start Date = 01/06/2026 and PrescOn = 01/06/2026.<br>3. Create Work Order C with Rental Start Date = 01/06/2026 and PrescOn = 30/05/2026.<br>4. Generate invoices from all three Work Orders. | **Verify after step #4:**<br>• All three Work Orders can be completed.<br>• All three invoices are generated.<br>• No save validation blocks Rental Start Date `<`, `=`, or `>` PrescOn. | • No DVA XML export rule is applied during Work Order save or invoice generation.<br>• Source Rental Start Date remains the value entered/generated from Work Order data. | Chrome / Edge on Desktop | • Required date fields are readable and keyboard reachable. | Confirms this ticket must not add Work Order date validation. |

## Group 1 - CP Web -> Raptor DVA Submissions -> Export Invoice XML

Scope: Export Invoice XML only. Validation / Errors column / IVL027 are out of scope.

| TC ID | Priority | Feature | Test Area | Title | Preconditions | Test Steps | Expected Result | Expected Integration | Browser/Device | Accessibility Check | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC-SMAR2633-WEB-001 | High | DVA Invoice Export | CP Web -> Raptor DVA Submissions -> Export Invoice XML | Verify XML exports HireStartDate as PrescOn when Rental Start Date is earlier than PrescOn | • DVA rental invoice exists in Raptor DVA Submissions<br>• Invoice is generated from a Work Order with rental item<br>• Rental Start Date = 01/06/2026<br>• PrescOn = 03/06/2026<br>• Invoice is available for XML export | 1. Login to CP Web.<br>2. Go to Raptor DVA Submissions.<br>3. Search/filter the prepared invoice.<br>4. Select the invoice.<br>5. Export the invoice XML.<br>6. Open/download the generated XML file.<br>7. Locate the invoice/rental item node and review `HireStartDate` and `DateLastPresc`. | **Verify after step #7:**<br>• XML is generated successfully.<br>• `HireStartDate` = 03/06/2026.<br>• `DateLastPresc` = 03/06/2026.<br>• `HireStartDate` is not exported as original Rental Start Date 01/06/2026.<br>• Export does not fail when Rental Start Date is earlier than PrescOn. | • XML export service applies export-only rule: `RentalStartAt < PrescOn -> HireStartDate = PrescOn`.<br>• No invoice, Work Order, or Prior Approval source data is updated by export.<br>• Existing XML structure remains unchanged except calculated `HireStartDate`. | Chrome / Edge on Desktop | • Export button is keyboard reachable.<br>• Export/download result is visible and readable. | Main ticket scenario. |
| TC-SMAR2633-WEB-002 | High | DVA Invoice Export | CP Web -> Raptor DVA Submissions -> Export Invoice XML | Verify XML exports HireStartDate unchanged when Rental Start Date equals PrescOn | • DVA rental invoice exists in Raptor DVA Submissions<br>• Rental Start Date = 01/06/2026<br>• PrescOn = 01/06/2026<br>• Invoice is available for XML export | 1. Login to CP Web.<br>2. Go to Raptor DVA Submissions.<br>3. Search/filter the prepared invoice.<br>4. Select the invoice.<br>5. Export the invoice XML.<br>6. Open/download the generated XML file.<br>7. Locate the invoice/rental item node and review `HireStartDate` and `DateLastPresc`. | **Verify after step #7:**<br>• XML is generated successfully.<br>• `HireStartDate` = 01/06/2026.<br>• `DateLastPresc` = 01/06/2026.<br>• No unnecessary date adjustment occurs when both dates are equal.<br>• `HireStartDate` is not blank, removed, duplicated, or shifted to another date. | • XML export service keeps `HireStartDate` as Rental Start Date when Rental Start Date equals PrescOn.<br>• No invoice/source data update API is triggered by export.<br>• Existing valid equal-date invoice export behavior is preserved. | Chrome / Edge on Desktop | • Selected invoice remains visibly selected before export.<br>• Export feedback is not dependent on color only. | Boundary valid case. |
| TC-SMAR2633-WEB-003 | High | DVA Invoice Export | CP Web -> Raptor DVA Submissions -> Export Invoice XML | Verify XML exports HireStartDate as Rental Start Date when Rental Start Date is later than PrescOn | • DVA rental invoice exists in Raptor DVA Submissions<br>• Rental Start Date = 01/06/2026<br>• PrescOn = 30/05/2026<br>• Invoice is available for XML export | 1. Login to CP Web.<br>2. Go to Raptor DVA Submissions.<br>3. Search/filter the prepared invoice.<br>4. Select the invoice.<br>5. Export the invoice XML.<br>6. Open/download the generated XML file.<br>7. Locate the invoice/rental item node and review `HireStartDate` and `DateLastPresc`. | **Verify after step #7:**<br>• XML is generated successfully.<br>• `HireStartDate` = 01/06/2026.<br>• `DateLastPresc` = 30/05/2026.<br>• `HireStartDate` is not incorrectly replaced with PrescOn.<br>• `HireStartDate` remains later than `DateLastPresc` based on date-only comparison. | • XML export service applies the rule only when `RentalStartAt < PrescOn`.<br>• Existing valid DVA rental invoice export behavior is preserved.<br>• No invoice/source data update API is triggered by export. | Chrome / Edge on Desktop | • Export action can be completed without mouse-only dependency.<br>• Generated file/download feedback is readable. | Regression case. |

## Group 2 - CP Web -> Raptor DVA Submissions -> Batch Export Invoice XML

Scope: Multiple selected DVA rental invoices. Each invoice must calculate independently.

| TC ID | Priority | Feature | Test Area | Title | Preconditions | Test Steps | Expected Result | Expected Integration | Browser/Device | Accessibility Check | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC-SMAR2633-WEB-004 | High | DVA Invoice Export | CP Web -> Raptor DVA Submissions -> Export Invoice XML | Verify XML applies HireStartDate logic independently when exporting multiple selected invoices with different Rental Start Date values | • Multiple DVA rental invoices exist in Raptor DVA Submissions<br>• Invoice A: Rental Start Date = 01/06/2026, PrescOn = 03/06/2026<br>• Invoice B: Rental Start Date = 01/06/2026, PrescOn = 01/06/2026<br>• Invoice C: Rental Start Date = 01/06/2026, PrescOn = 30/05/2026<br>• Each invoice can be identified in XML by invoice number/client/device/item details | 1. Login to CP Web.<br>2. Go to Raptor DVA Submissions.<br>3. Search/filter and confirm Invoice A, Invoice B, and Invoice C are listed.<br>4. Select all three prepared invoices.<br>5. Export the selected invoices to XML.<br>6. Open/download the generated XML file.<br>7. Locate each invoice node in the XML.<br>8. Review `HireStartDate` and `DateLastPresc` for each exported invoice. | **Verify after step #8:**<br>• XML is generated successfully for all selected invoices.<br>• Invoice A exports `HireStartDate` = 03/06/2026 and `DateLastPresc` = 03/06/2026.<br>• Invoice B exports `HireStartDate` = 01/06/2026 and `DateLastPresc` = 01/06/2026.<br>• Invoice C exports `HireStartDate` = 01/06/2026 and `DateLastPresc` = 30/05/2026.<br>• One invoice's calculated `HireStartDate` does not overwrite or affect another invoice's XML values.<br>• No selected invoice is missing, duplicated, or exported with another invoice's dates. | • XML export service calculates `HireStartDate` independently per selected invoice.<br>• Batch export does not reuse the first invoice's PrescOn/Rental Start Date for other invoices.<br>• Existing XML structure and invoice identifiers remain stable for each exported invoice.<br>• No invoice, Work Order, or Prior Approval source data is updated by XML export. | Chrome / Edge on Desktop | • Multiple selected invoices remain visibly selected before export.<br>• Export/download feedback is visible and not dependent on color only. | Covers batch export risk. |

## Group 3 - CP Web -> Invoice Source Detail -> Export XML Does Not Persist Adjustment

Scope: XML transformation only. UI/database/source values must remain unchanged.

| TC ID | Priority | Feature | Test Area | Title | Preconditions | Test Steps | Expected Result | Expected Integration | Browser/Device | Accessibility Check | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC-SMAR2633-WEB-005 | High | DVA Invoice Export | CP Web -> Raptor DVA Submissions -> Export Invoice XML | Verify XML export does not update invoice Rental Start Date in UI/source data when HireStartDate is adjusted | • DVA rental invoice exists in Raptor DVA Submissions<br>• Invoice is generated from a Work Order with rental item<br>• Rental Start Date = 01/06/2026<br>• PrescOn = 03/06/2026<br>• User can access invoice/source detail after export | 1. Login to CP Web.<br>2. Open the invoice/source detail and record the displayed Rental Start Date and PrescOn.<br>3. Go to Raptor DVA Submissions.<br>4. Search/filter the prepared invoice.<br>5. Select the invoice.<br>6. Export the invoice XML.<br>7. Confirm the XML values for `HireStartDate` and `DateLastPresc`.<br>8. Reopen/refresh the invoice/source detail.<br>9. Review the Rental Start Date and PrescOn again. | **Verify after step #2:**<br>• UI/source Rental Start Date = 01/06/2026.<br>• PrescOn = 03/06/2026.<br><br>**Verify after step #7:**<br>• XML `HireStartDate` = 03/06/2026.<br>• XML `DateLastPresc` = 03/06/2026.<br><br>**Verify after step #9:**<br>• UI/source Rental Start Date still = 01/06/2026.<br>• PrescOn still = 03/06/2026.<br>• Export does not silently edit invoice, Work Order, or Prior Approval source values. | • Export transformation is export-only and is not persisted to invoice/source records.<br>• No invoice edit/save API is triggered by XML export.<br>• No Document Change Log or invoice edit audit record is created only because of export. | Chrome / Edge on Desktop | • User can return to invoice/source detail after export without losing context.<br>• Date values remain visible and readable after refresh/reopen. | Data integrity regression case. |

## Group 4 - CP Web -> Raptor DVA Submissions -> Purchase Item Regression

Scope: DVA purchase items are out of scope for the new rental `HireStartDate` rule.

| TC ID | Priority | Feature | Test Area | Title | Preconditions | Test Steps | Expected Result | Expected Integration | Browser/Device | Accessibility Check | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC-SMAR2633-WEB-006 | High | DVA Invoice Export | CP Web -> Raptor DVA Submissions -> Export Invoice XML | Verify DVA purchase item XML does not apply the rental HireStartDate adjustment rule | • DVA purchase invoice exists in Raptor DVA Submissions<br>• Purchase invoice has PrescOn = 03/06/2026<br>• Purchase item has existing export behavior available for comparison<br>• Invoice is available for XML export | 1. Login to CP Web.<br>2. Go to Raptor DVA Submissions.<br>3. Search/filter the prepared DVA purchase invoice.<br>4. Select the purchase invoice.<br>5. Export the invoice XML.<br>6. Open/download the generated XML file.<br>7. Locate the purchase item node and review date fields relevant to existing purchase export behavior. | **Verify after step #7:**<br>• XML is generated successfully.<br>• Purchase item does not apply `RentalStartAt < PrescOn -> HireStartDate = PrescOn` rental logic.<br>• Purchase item date fields follow existing purchase XML export behavior.<br>• Purchase item is not missing, duplicated, or incorrectly converted to a rental item in XML. | • XML export service limits the new `HireStartDate` adjustment to rental items only.<br>• No purchase item source data is updated by export.<br>• Existing purchase XML structure remains unchanged. | Chrome / Edge on Desktop | • Purchase invoice can be selected and exported without mouse-only dependency.<br>• Export/download feedback is readable. | Exact purchase XML date field behavior is existing behavior / `Needs confirmation` if no baseline XML is available. |

## Group 5 - CP Web -> Raptor DVA Submissions -> Date-Only Comparison

Scope: Date-only comparison. Use this only when QA can prepare or inspect hidden time values.

| TC ID | Priority | Feature | Test Area | Title | Preconditions | Test Steps | Expected Result | Expected Integration | Browser/Device | Accessibility Check | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TC-SMAR2633-WEB-007 | Medium | DVA Invoice Export | CP Web -> Raptor DVA Submissions -> Export Invoice XML | Verify XML compares Rental Start Date and PrescOn by calendar date only when hidden times differ | • DVA rental invoice exists in Raptor DVA Submissions<br>• Rental Start Date calendar date = 01/06/2026<br>• PrescOn calendar date = 01/06/2026<br>• Test data has different hidden datetime values behind those same calendar dates, if controllable<br>• Invoice is available for XML export | 1. Login to CP Web.<br>2. Go to Raptor DVA Submissions.<br>3. Search/filter the prepared invoice.<br>4. Select the invoice.<br>5. Export the invoice XML.<br>6. Open/download the generated XML file.<br>7. Locate the invoice/rental item node and review `HireStartDate` and `DateLastPresc`. | **Verify after step #7:**<br>• XML is generated successfully.<br>• `HireStartDate` = 01/06/2026.<br>• `DateLastPresc` = 01/06/2026.<br>• Export treats the two values as equal because the calendar date is the same.<br>• `HireStartDate` is not shifted due to hidden time, server timezone, or UTC conversion. | • XML export service compares date portion only for this rule.<br>• No invoice/source data update API is triggered by export.<br>• Existing XML date format remains consistent with DVA export behavior. | Chrome / Edge on Desktop | • Date values in UI/XML remain readable and not ambiguous. | Execute only if hidden time setup is possible; otherwise keep as risk-based regression note. |
