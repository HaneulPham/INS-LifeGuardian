# INS LifeGuardian New Service Request Steps for Peripherals QA Context

This document is supporting QA evidence for SMAR-2537. Current Jira requirements and verified API/integration contracts take precedence. Conflicts and unspecified behavior are marked `Needs confirmation`.

## Purpose and authority

- Feature: New Service Request Steps for Peripherals.
- Source ticket: SMAR-2537.
- Related historical ticket: SMAR-2531, which temporarily removed peripheral `Listen for Alarm` because the Service Request workflow could not attribute an alarm reliably.
- Evidence reviewed: six supplied Jira requirement and reference screenshots on 24/06/2026.
- The screenshots describe requirements and design references; they do not prove implementation or execution results on a particular build.

## Feature purpose

SMAR-2537 adds `Generate Medi Alarm` and `Listen for Alarm` to peripheral Device Setup Steps and to the Service Request Progress workflow. The medi-alarm record provides an identity that can be used to attribute an incoming peripheral alarm to the intended client file, parent/main device, and medi alarm.

This supersedes the earlier general restriction that `Listen for Alarm` is unavailable for peripherals, but only for the explicitly supported peripheral types and only when the new dependency chain is satisfied.

## Platforms and components

- CP Device Setup Steps configuration for peripherals.
- CP Service Request Progress tab and peripheral checklist instances.
- Parent/main device assignment to a client file.
- Client File `Medi-Alarm Devices` and `Home Security Devices` tabs.
- Alarm ingestion and matching, including AWS-hosted medi-alarm UUID identity and mobile backward compatibility.
- Service Request/checklist persistence, audit/history, and alarm records.
- No Portal, SOS Mobile, Carer App, report, export, or public API behavior is defined by the supplied evidence.

## Roles and permissions

- SMAR-2537 does not define which roles may configure the two step types, create a medi-alarm device, or start/cancel a listener. `Needs confirmation`.
- Existing Service Request rules should continue to restrict Process actions to the assigned, authorized user; whether any feature-specific permission is also required is `Needs confirmation`.
- Direct UI, API, or service calls must not permit cross-file or cross-tenant medi-alarm creation or alarm matching. This is a QA security requirement inferred from the linkage rules, not a supplied endpoint contract.

## Terminology and data model

- The requirement uses both `Generate Medi Alarm` and the section heading `Create Medi Alarm`. The exact configured step label and Progress-tab label are `Needs confirmation`.
- Medi Alarm Type is configured on the peripheral Device Setup Step. The supplied types are `CAMS` and `INS`.
- The reference UI shows more specific selectable values such as `Call Point CAMS` and `Call Point INS01`; the permitted type list, mapping from these values to CAMS/INS, and whether the examples are current are `Needs confirmation`.
- `Owner` means a client selectable from the client file assigned through the parent/main device workflow.
- For CAMS, the user-facing `Zone No` and INS `Location` use the same internal field. The actual backend key is `Needs confirmation`.
- Alarm field `RecivedFromMediAlarmDeviceId` is intentionally misspelled in the existing contract and stores a GUID/UUID rather than a numeric ID. Renaming or changing its type could break mobile backward compatibility.
- The listener compares `RecivedFromMediAlarmDeviceId` on the received alarm with the created medi alarm's `Uuid`.

## Supported peripherals

The two steps apply only to these ticket-listed peripheral types:

- `BrooksSmoke240v`
- `BrooksSmoke240vLithium`
- `LSeriesSmoke240v`
- `SmartlinkSmoke240v`
- `Smoke9v`
- `LSeriesTransmitter`
- `LSeriesTransmitterF1`
- `SmartlinkTransmitter`
- `LSeriesFallSensor`
- `SmartlinkFallSensor`
- `ChiptechPearlFallSensor`
- `LSeriesCallPoint`
- `SmartlinkCallPoint`
- `MiaPendant`
- `LSeriesSmokeTransmitter`
- `SmartlinkSmokeTransmitter`
- `ChiptechPearlNeckTransmitter`
- `ChiptechPearlWatchTransmitter`

`PIR` appears in the source list with an explicit author comment questioning whether it sends an alarm. Its inclusion is `Needs confirmation`; do not treat it as supported until that comment is resolved.

Other peripheral types must not expose or accept these steps unless a later requirement adds them.

## Workflows and state transitions

### Device Setup configuration

1. An authorized user selects a supported peripheral mapping.
2. `Generate Medi Alarm` is available as a step type.
3. Its configuration requires Medi Alarm Type.
4. The configuration is valid only when the parent/main device workflow contains `Assign to Client File` before the peripheral medi-alarm step.
5. `Listen for Alarm` is available as a peripheral step type and has no additional configuration fields.
6. `Listen for Alarm` requires `Generate Medi Alarm` before it.

Required chain:

`Parent/main device: Assign to Client File -> Peripheral: Generate Medi Alarm -> Peripheral: Listen for Alarm`

How cross-device dependency validation is presented, and whether invalid reorder/delete/save operations are blocked, is `Needs confirmation`.

### Service Request Progress: generate medi alarm

1. The step uses the Medi Alarm Type saved in Device Setup configuration.
2. The UI provides `Description` for both CAMS and INS.
3. The UI provides `Zone No` for CAMS or `Location` for INS.
4. The UI provides an `Owner` dropdown for both types, restricted to clients belonging to the parent/main device's assigned client file.
5. `Create` remains disabled until all applicable fields are populated.
6. A successful Create action creates one medi-alarm device linked to the selected file and client.
7. The created device appears under either the Client File `Medi-Alarm Devices` tab or `Home Security Devices` tab according to its type.

The exact type-to-tab mapping is `Needs confirmation`.

### Service Request Progress: listen for alarm

1. `Listen for Alarm` becomes available only after the medi alarm has been created successfully.
2. Selecting `Listen for Alarm` starts a waiting/listening state for that specific checklist instance and medi alarm.
3. A received alarm completes or satisfies the listener only when it matches the intended file, parent/main device, and medi alarm.
4. Medi-alarm identity matching compares the alarm's `RecivedFromMediAlarmDeviceId` value to the medi alarm's `Uuid`.
5. An alarm for another file, main device, medi alarm, peripheral instance, or Service Request must not complete this step.

The exact waiting, success, timeout, retry, cancellation, and manual-completion states are `Needs confirmation`.

## UI behavior

### CAMS medi alarm

- Fields explicitly required on Progress: `Description`, `Zone No`, and `Owner`.
- The reference screenshot shows a medi-alarm Type selector such as `Call Point CAMS`, but the ticket says Type is assigned in Device Setup. Whether Type is displayed read-only, selectable, or omitted on Progress is `Needs confirmation`.

### INS medi alarm

- Fields explicitly required on Progress: `Description`, `Location`, and `Owner`.
- The reference screenshot also shows `Guard Timer (seconds)`, `Silent Alarm`, `Strobe Light`, `All House Lights On`, and `All Power Points Off`. An annotation says these fields must be included either in Device Setup or on the Service Request, but the written acceptance criteria omit them and say Device Setup requires only Type. Their presence, defaults, validation, storage location, and required/optional status are `Needs confirmation`.
- The screenshot example shows Guard Timer defaulting to `10`; this is reference evidence, not a confirmed default or boundary.

### General validation

- All applicable fields must be populated before `Create` is enabled.
- Exact whitespace handling, field lengths, allowed characters, numeric boundaries, duplicate-name rules, validation messages, and Owner empty-state behavior are `Needs confirmation`.
- Closing/cancelling the create UI must not create or partially link a medi-alarm record. This is a QA assumption based on data-integrity expectations.

## Backend and API behavior

- No endpoint, method, request schema, response status, or persistence schema is supplied; all are `Needs confirmation`.
- Creation must persist the medi alarm once and link it to the correct file and client.
- Listener registration and callback handling must be idempotent: repeated clicks, duplicate alarm delivery, retries, or reconnects must not create duplicate medi alarms, listeners, checklist completions, or alarm relationships. This is a required QA posture, not an explicit API contract.
- A failed create operation must not leave an orphan medi alarm or partial file/client association.
- Matching must use the created medi alarm UUID and preserve the legacy `RecivedFromMediAlarmDeviceId` contract for backward compatibility.
- The requirement separately states that file and parent/main device must match, but the technical note only explains UUID matching. The authoritative source of the file and parent-device checks is `Needs confirmation`.

## Jobs, queues, and timing

- The mechanism used to register the listener and deliver alarms is not supplied.
- Listener timeout, polling/subscription duration, recovery after CP restart, delayed alarms, out-of-order alarms, queue retry, duplicate delivery, and concurrent listeners are `Needs confirmation`.
- QA must verify exactly-once completion and that a late or retried unrelated alarm cannot satisfy a different checklist instance.

## Notifications and integrations

- Alarm ingestion and AWS medi-alarm identity are directly affected.
- Mobile backward compatibility depends on retaining the legacy alarm field name and UUID value semantics.
- No FCM, SMS, email, Twilio, CAMS external-call behavior, recipient, or notification-log requirement is defined for these two steps.
- Despite the `CAMS` label, whether medi-alarm creation calls an external CAMS service is `Needs confirmation`; do not equate this step with the existing `Generate CAMS Asset` step.

## Reports, exports, audit, and history

- No report or export behavior is specified.
- Audit/history expectations for configuration changes, medi-alarm creation, Owner selection, listener start, matched/rejected alarms, completion, retry, or failure are `Needs confirmation`.
- Existing Service Request progress/history must retain the created medi alarm and completion state after refresh/reopen and normal status transitions. This is a regression expectation inferred from existing checklist snapshot behavior.

## Data integrity and security

- The medi alarm must link to exactly the selected Owner and the correct assigned file; client data from another file or tenant must never be selectable or linked.
- Multiple peripherals under the same parent must retain distinct medi-alarm UUIDs and listener state.
- A matching alarm must not complete more than its intended peripheral checklist instance.
- Repeated Create must not create duplicate medi-alarm devices.
- Editing/removing a configured step, reducing item quantity, removing the peripheral, reassigning the parent device, cancelling the Service Request, or deleting/unlinking the medi alarm could create orphan listener or linkage data. Cleanup/migration rules are `Needs confirmation`.
- Existing Service Requests created while SMAR-2531 excluded peripheral listening must not gain, lose, or reorder snapshotted steps unexpectedly. Whether SMAR-2537 applies only to new requests or migrates untouched existing requests is `Needs confirmation`.

## Confirmed validation themes

- Availability is restricted to the confirmed peripheral allowlist and relevant parent-device mapping.
- Dependency enforcement covers initial add, reorder, deletion, save, reload, and runtime execution.
- CAMS and INS render only their applicable labels and fields.
- Create-button enablement follows completion of every applicable field.
- Owner choices remain within the assigned file and the created record persists under the correct client.
- Creation is exactly once and visible in the correct Client File device tab.
- Listener matching accepts the intended file, main device, and medi-alarm UUID and rejects near matches and unrelated concurrent alarms.
- Duplicate clicks and duplicate/retried alarm messages do not create duplicate effects.
- Refresh/reopen and Service Request status transitions preserve medi-alarm linkage and step state.
- Existing main-device `Listen for Alarm`, `Generate CAMS Asset`, and unrelated peripheral workflows do not regress.

## Open questions and source conflicts

1. Is `PIR` supported, or must it be removed from the allowlist because it does not send an alarm?
2. Is the exact step label `Generate Medi Alarm` or `Create Medi Alarm`?
3. What are all valid Medi Alarm Type values, and how do specific values such as `Call Point CAMS` and `Call Point INS01` map to CAMS/INS behavior and Client File tabs?
4. For INS, where are Guard Timer and the four alarm/action toggles configured, and what are their defaults, validation rules, and required/optional status?
5. Is Type selectable on Service Request Progress, or fixed/read-only from Device Setup configuration?
6. Which clients must appear in Owner when the assigned file contains one, multiple, inactive, or no eligible clients? The screenshot value `Home` also needs definition.
7. What validation messages and field constraints apply to Description, Location/Zone No, Owner, Guard Timer, and Type?
8. How is the cross-device dependency on the parent/main `Assign to Client File` validated during add, reorder, delete, and runtime execution?
9. What exact matching properties prove file and parent/main-device identity in addition to the medi-alarm UUID comparison?
10. What are listener waiting, timeout, cancel, retry, failure, manual-completion, reconnect, and late-alarm behaviors?
11. Which audit/history/log records are required for configuration, creation, listener registration, rejected alarms, matched alarms, retries, and completion?
12. What cleanup applies when a peripheral or item is removed, quantity is reduced, the medi alarm is deleted, the parent is reassigned, or the Service Request is cancelled?
13. Does the change affect only new Service Requests, or are existing unstarted/snapshotted requests migrated?
14. Which roles/permissions may configure and execute the steps, and what API/service authorization protects the same operations?

## Required QA posture

- Treat this as a safety-sensitive attribution workflow: a false positive can validate the wrong installed device, while a false negative can block commissioning of a working alarm.
- Test each supported peripheral family and at least one unsupported peripheral; do not assume a single transmitter proves every mapping.
- Test CAMS and INS separately because their fields, labels, and target Client File tabs differ.
- Create concurrent listeners under the same file, different files, the same parent, and different parents to prove isolation.
- Reconcile the Progress UI, medi-alarm record, client/file linkage, stored UUID, received alarm, listener state, and checklist completion.
- Verify no-side-effect and recovery behavior for validation failures, create failures, listener registration failures, duplicate delivery, delayed delivery, and CP restart.
- Preserve the older SMAR-2531 restriction as historical context; apply SMAR-2537 only where its new allowlist and dependency chain are satisfied.
