# INS LifeGuardian Service Request QA Context

Use this document as supporting project knowledge when analyzing Service Requests, Work Orders, Device Setup Steps, device checklists, assets, SIM activation, CAMS, installation reporting, cancellation, or related inventory behavior.

This document summarizes supplied QA evidence. It is not a replacement for current Jira acceptance criteria, API contracts, production configuration, or current workflow definitions. Conflicting or uncertain items are marked `Needs confirmation`.

## Source documents

- SMAR-1516: Service Request Device Setup Checklists
- SMAR-2271: Cancel Service Request Option
- SMAR-2415: Services Install Summary Report Modifications
- Source PDFs were supplied and reviewed on 23/06/2026.

## Evidence interpretation

- Treat approved test intent and repeated behavior across the sources as strong project context.
- Do not treat a historical `PASS`, `FAIL`, `BLOCKED`, `REJECTED`, or `SKIP` result as proof of current production behavior.
- Do not reuse client files, service-request numbers, usernames, screenshots, or other identifying test data from the source documents.
- Related-ticket comments inside the test exports may represent later design corrections. Prefer the latest clearly stated rule, but retain conflicts as `Needs confirmation`.
- Do not invent Service Request API endpoints or schemas; the supplied documents focus mainly on CP behavior and integrations.

## Feature purpose and scope

Service Requests coordinate operational work against a client file or device. Depending on Service Request type, the workflow can allocate items, generate device-specific checklist instances, create assets, assign devices to client files, create CAMS assets, activate SIMs, listen for alarms, print labels, link devices and clients, dispatch work, invoice it, close it, or cancel it with inventory reversal.

Relevant areas include:

- CP Desktop Client File Details
- Client File Device Tree
- Service Requests and Associated Service Requests grids
- Service Request details, edit screen, Process tab, and Linked tab
- Administration/Settings - Device Setup Steps
- Asset Management, Stock Levels, and Transaction History
- Device records and client-file assignment
- CAMS
- Jasper SIM integration
- Alarm monitoring and callbacks
- Label printers and print dialogs
- Work Orders reports and exported report files
- Village Profit and Item Profit reports

## Service Request discovery and grids

- A device in Client File Device Tree exposes its linked Service Requests.
- Opening a device-level Service Requests view shows requests linked to that device and an empty state when none exist.
- Client File Details contains Service Requests management with direct and associated request presentation.
- A direct Service Request is created under the current client file.
- An associated Service Request can appear because a generated/linked device is assigned to another client file.
- The same request must not be duplicated within a grid or displayed in both direct and associated grids for the same context.
- Legacy request types such as Faulty Equipment, Faulty Power Pack, and Billing remain accessible in supplied coverage. Current create/edit availability requires confirmation.

## Service Request types and checklist behavior

### Technical Issue

- Creating a Technical Issue does not load a Device Setup checklist.
- Process displays no device checklist steps for this type.
- Items behave as standard Service Request items without checklist instances.
- The request remains linked only to the selected device and must not appear beneath unrelated devices.
- During edit, an existing Technical Issue can display its current type, but Technical Issue is not offered as a selectable target type.
- Supplied coverage allows an Open Technical Issue to change to New Install or Repair Devices, which then generates the applicable checklist.
- A Technical Issue is not allowed to move to Under Review in the supplied tests. Confirm the current intended status path.

### New Install

- Device checklist groups are generated from Device Setup Steps - New Install configuration.
- Checklist instance quantity matches each item quantity.
- Different item types receive separate checklist groups.

### Repair Devices

- Device checklist groups are generated from Device Setup Steps - Repair Device configuration.
- Checklist instance quantity matches each item quantity.
- Different item types receive separate checklist groups.

The source alternates between `RepairDevice`, `Repair Devices`, and `RepairDevices`. Confirm exact UI label and backend enum before using literal values.

### Billing

- Existing Billing requests remain accessible.
- Billing type cannot be changed to New Install or Repair Devices in supplied edit coverage.

## Type-editing rules

- Open Technical Issue can change to New Install or Repair Devices.
- Open New Install can change to Repair Devices.
- Open Repair Devices can change to New Install.
- Technical Issue is not a selectable target type in the edit dropdown.
- Billing is immutable in the supplied coverage.
- Type is locked once status is In Progress, Dispatch, Invoicing, or Closed.
- A rejected type change must not reset item data, checklist progress, asset assignment, or linked-device state.

## Item quantity and checklist synchronization

- One device checklist instance is created per item quantity unit.
- Increasing quantity creates additional instances while preserving progress on existing instances.
- Adding another device item creates a new checklist group using the correct configuration.
- Removing an item removes only its checklist instances; unrelated groups and progress remain unchanged.
- Reducing quantity after processing requires the user to identify which device instance is removed when multiple instances exist.
- Completed device details and remaining checklist history must not be blanked, duplicated, or reassigned accidentally.

### Removing an item after asset/device processing

- The removed checklist instance disappears from the Service Request.
- The asset record remains in the system.
- The device is unlinked from the Service Request item and unassigned from the client file.
- No orphan checklist linkage remains.

### Removing an item after SIM activation

- The asset/device record remains.
- Device-client and Service Request item links are removed.
- The SIM is no longer active and is reset to an activation-ready state in the supplied coverage.
- Jasper customer/service association is cleared while CP retains ICCID and line-number information.
- Exact Jasper status labels and cleanup behavior must be confirmed from the current integration contract.

## Process tab access and execution

- Open and Under Review requests show checklists but keep action controls disabled.
- In Progress enables checklist execution.
- Only the user assigned to the Service Request can action checklist steps; other users may view and expand the checklist but cannot execute actions.
- Unauthorized attempts must not create assets, assignments, CAMS records, SIM actions, print jobs, listeners, or activity side effects.
- Each checklist instance maintains its own asset, device, and completion state.
- Completed steps persist after refresh/reopen.

## Device Setup Steps configuration

- Configuration is separated by service type: New Install and Repair Device.
- Configuration is mapped by device type.
- Peripheral configuration is additionally mapped by parent main device or `None`.
- Switching device, peripheral, parent mapping, or service-type tab must load only the matching configuration without mixing cached steps.
- Duplicate non-custom steps for the same device/service-type mapping are rejected.
- Custom Steps may be repeated when their business identity is intentionally different; exact duplicate-title rules require confirmation.

### Available step types

The supplied configuration coverage includes:

1. Generate Asset
2. Assign to Client File
3. Generate CAMS Asset
4. Activate SIM
5. Listen for Alarm
6. Print Label
7. Custom Step

### Dependency rules

- When Generate Asset exists, it must precede Assign to Client File.
- Assign to Client File may exist without Generate Asset according to the later SMAR-2520 correction.
- Generate CAMS Asset requires Generate Asset and must come after it.
- Activate SIM requires Assign to Client File and must come after it.
- Listen for Alarm requires Assign to Client File and must come after it.
- Print Label and Custom Step are described as flexibly orderable in configuration.
- Runtime execution still follows checklist order and can keep a step disabled while an earlier required step remains incomplete.
- Invalid add/reorder/delete operations must leave the saved configuration unchanged.

### Current peripheral restrictions

- Custom Step is supported for peripherals.
- The later SMAR-2531-related coverage states that Listen for Alarm is not available for peripherals because an alarm cannot be reliably attributed to a specific peripheral.
- Earlier cases that allowed peripheral Listen for Alarm were skipped/superseded and must not be treated as the current rule.
- Supplied coverage expects Print Label only for main devices, not peripherals.

### Checklist snapshot behavior

- A Service Request snapshots the checklist used for its process workflow.
- Reordering or deleting Device Setup Steps must not retroactively change an existing request after checklist progress exists.
- Existing completed/incomplete states and original order remain unchanged.
- A new Service Request uses the latest saved setup configuration.

## Process step behavior

### Generate Asset

- Creates one asset/device record for the current checklist instance.
- Displays the generated asset barcode and marks the step complete.
- Enables barcode printing after generation.
- Retrying after success must not create another asset.
- Another checklist instance creates a different asset and barcode.
- Failure leaves the step incomplete, creates no asset/device record, and permits retry.
- A valid pre-existing barcode can be used for printing without auto-generating an asset in supplied coverage.

### Assign to Client File

- Uses the generated asset barcode automatically when available.
- Allows selection of the target client file.
- Successful assignment marks the step complete and disables repeated assignment.
- The device appears in the target Client File Device Tree.
- Linked Clients and Linked Devices update to reflect the assignment.
- Assignment failure must not clear entered barcode/selection unnecessarily and must allow correction/retry.

### Generate CAMS Asset

- Cannot execute before required asset/assignment prerequisites.
- Calls CAMS and stores/displays the returned CAMS Asset Number.
- The same CAMS Asset Number appears in Process, CP device record, and CAMS.
- CAMS failure creates no CAMS record, leaves the step incomplete, displays an error, and permits retry.

### Activate SIM

- Cannot execute before required preceding steps.
- Requires an ICCID.
- Blank ICCID shows `Unable to update SIM details` with detail equivalent to `No ICCID has been entered` in supplied coverage.
- Successful activation calls Jasper, marks the step complete, updates SIM status to Active in CP, and updates ICCID/line number on the device record.
- Invalid/non-existent ICCID fails without completing the step or creating an activation record.
- Source comments indicate previously active, deleted, suspended, or deactivated SIM handling changed during testing. Confirm current reactivation rules before writing literal expectations.

### Listen for Alarm

- Cannot execute before required preceding steps.
- Starts one listening session for the main device.
- Repeated clicks must not create duplicate listeners or callbacks.
- An alarm from the expected device completes the step once and records the alarm/callback relationship.
- An alarm from another device or another client file must not complete the waiting step.
- Without an alarm, the step remains waiting and may support manual completion.
- Current intended configuration excludes this step for peripherals.

### Print Label

- Supported label coverage includes Front Box Label, Back Box Label, and Service Request Barcode.
- Printed values can include village, client/unit, asset code, CAMS asset number, device code, callback number, SIM ICCID, Service Request barcode, and Service Request ID depending on template.
- Printing must not mutate asset/device records.
- Print uses the configured label printer and opens the supported print dialog.
- The sources conflict on whether Print Label can be configured/executed without Assign to Client File. Treat the exact prerequisite as `Needs confirmation`.

### Custom Step

- Supported for main devices and peripherals.
- Contains a title and description; supplied coverage uses a 50-character title boundary.
- Is manually completed and triggers no automation unless a later requirement defines it.
- Completing one peripheral Custom Step must not affect the main device or another peripheral instance.

## Linked tab

- Always shows Linked Clients and Linked Devices sections, including empty states.
- Linked Clients can include the original Service Request client and other clients receiving devices generated through the request.
- Linked Devices lists each generated/linked device and its assigned client file.
- Client cards are unique even when multiple devices are assigned to the same client.
- Cross-client device mapping must not leak or mix client data.
- Removing the last linked device for a client removes that client from Linked Clients.
- Reassignment updates the device-to-client mapping.
- Selecting a linked device can navigate to the client file that currently owns the device, even when different from the original Service Request file.
- Source tests show some historical failure/skip evidence for removal and reassignment synchronization; revalidate on the target build.

## Status workflow and restrictions

The full workflow used for New Install and Repair Devices is:

`In Progress -> Dispatch -> Invoicing -> Closed`

Additional earlier states include `Open` and `Under Review` where applicable.

- Checklist actions are disabled in Open and Under Review.
- Moving from In Progress to Dispatch requires all device-item checkboxes/required processing to be complete.
- Dispatch locks item add/remove/quantity changes.
- Invoicing locks item add/remove/quantity changes.
- Closed is terminal and read-only.
- Checklist progress, assigned devices, barcodes, client relationships, SIM/CAMS/alarm data, and history remain intact across status transitions.
- Status transitions must not create duplicate Service Requests, assets, devices, or checklist records.

## Cancellation

### UI and status

- `Cancel Request` is a dedicated action beside `Close Request` in the supplied design.
- `Cancelled` is not selectable from the regular Move To status dropdown.
- A Cancelled filter exists under the status filters and appears after Closed in the supplied UI.
- Filtering by Cancelled returns only cancelled requests and supports an empty state.
- Cancellation is available from non-closed statuses in the supplied coverage.
- A cancellation note is mandatory.
- Successful cancellation sets status to `Cancelled`.
- The expected note format is `Service Request Cancelled by {username} - {note}`.
- Edit, Move To, Close Request, and further status-change actions become unavailable.
- Items remain visible but read-only.
- Cancelled status is displayed in red; non-cancelled status uses the normal/default styling.

### Inventory reversal

For each item attached to a successfully cancelled request:

- Allocated quantity is reduced by the quantity previously allocated to the request.
- Available quantity increases accordingly.
- Total stock quantity remains consistent.
- A Return transaction is created in Asset Management Transaction History.
- Transaction history identifies the reversal without duplicating stock movement.

If cancellation validation fails, no stock quantity or transaction record changes.

### Reporting and visibility

- Cancelled requests are excluded from Village Profit Report.
- Cancelled requests are excluded from Item Profit Report.
- Supplied coverage says cancelled requests should not appear on the Client File Details Service Requests tab, while they remain retrievable through the Cancelled filter/detail flow. Exact scope requires confirmation.

## Close Request

- Closed requests are terminal and read-only.
- Supplied coverage expects the note format `Service Request Closed by {username} - {note}`.
- Closing a request with allocated items is expected to reverse allocation and create Return transactions similarly to cancellation.
- SMAR-2271 TC#15 is internally inconsistent: its title/expected status describe Close Request, but its steps say to click Cancel Request. Confirm the correct action path before reusing this case.

## Services Installed Summary report

Path in the supplied tests:

`CP Web -> Reports -> Work Orders Reports -> Services Installed Summary`

### Columns and source data

- New columns: Price and Purchase Type.
- Price is sourced from Work Order item pricing rather than a generic product display price.
- Purchase Type values include `Purchase` and `Rental`.
- Report output is validated in the generated/exported report file.

### Grouping

- Matching rows with the same Product Code, Price, State, and Purchase Type are grouped.
- Quantity is summed across grouped records.
- The same product with different prices produces separate rows.
- Quantities must not merge across different price values or purchase types.

### Average calculations

- Average Purchase Price and Average Rental Price are calculated separately.
- The expected formula is quantity-weighted average, not an unweighted average of displayed rows.
- Example from the supplied tests: `(4 x $10.00 + 1 x $300.00) / 5 = $68.00`.
- Values are rounded to two decimal places using standard rounding.
- Zero-priced items must not cause NaN or divide-by-zero errors.
- Installed Date and Work Order Type filters restrict both report rows and the average dataset.

### Regression expectations

- Existing Services Installed and other Work Orders reports continue to render without unexpected totals/footer sections.
- New columns or calculations must not change unrelated reports.

## Open questions and source conflicts

1. **Price format:** SMAR-2415 expects `$xx.xx`, but execution notes say the missing currency format was accepted/bypassed. Confirm whether Price must include a currency symbol.
2. **Empty report:** one case title expects `$0.00` averages for an empty dataset, but the recorded behavior says no report is generated and was marked PASS. Confirm the intended empty-state contract.
3. **Work Order Type filter:** a case title references DVA while its steps select Private. Confirm the intended filter/value matrix.
4. **Cancel versus Close:** SMAR-2271 TC#15 describes Close but executes Cancel in the steps.
5. **Cancelled visibility:** clarify whether cancelled requests are hidden only from a client-file grid while still available globally through the Cancelled filter.
6. **Repair type naming:** confirm UI label and backend enum for Repair Device(s).
7. **Technical Issue workflow:** confirm why Technical Issue cannot move to Under Review and identify its valid lifecycle.
8. **Print Label prerequisites:** configuration tests allow independent placement, while Process tests disable it before assignment.
9. **Peripheral Listen for Alarm:** later evidence removes it; ensure old configurations and existing Service Requests migrate safely.
10. **SIM reactivation:** source comments supersede some invalid-status expectations. Confirm Jasper behavior for active, deactivated, suspended, deleted, or swapped SIMs.
11. **Associated Service Requests:** confirm exact rules for which client-file grid shows direct versus associated records after assignment or reassignment.
12. **API coverage:** no authoritative Service Request endpoint/schema was established by these sources.

## Required QA posture for future Service Request work

- Identify the request type, current status, assigned user, item quantities, device/peripheral mapping, and current checklist progress before defining expected behavior.
- Separate Service Request persistence from asset, device, inventory, CAMS, Jasper, alarm, print, report, and history side effects.
- Verify exactly-once behavior for asset creation, stock Return transactions, CAMS creation, SIM activation, listener registration, callbacks, labels, and status transitions.
- Verify rollback/no-side-effect behavior whenever validation or an external dependency fails.
- Cover direct and associated grids, cross-client mappings, Linked tab, Device Tree, and reopen/refresh persistence.
- Confirm whether Device Setup changes affect existing requests or only new requests; preserve snapshot behavior when progress exists.
- Test configuration dependencies both when adding steps and when reordering/deleting them.
- Test type/status transitions as a matrix rather than assuming every status is reachable from every type.
- For reports, reconcile source Work Order rows, grouping keys, filtered dataset, weighted calculation, formatting, and exported file values.
- Use current Jira requirements and integration/API contracts when they conflict with this historical QA evidence.
