# Reviewer and Rovo feedback workflow

Use this workflow when feedback is supplied for analysis, coverage groups, or existing test cases.

## 1. Parse each feedback item

Restate the requested change and identify the affected requirement, group, and case IDs. Compare it with current Jira/Confluence evidence, user-confirmed decisions, existing cases, and the active coverage plan.

## 2. Classify the decision

Use one of these decisions:

- **Add** — a distinct missing rule, boundary, failure mode, integration, or regression risk.
- **Update** — the existing case has the right objective but needs corrected steps, data, assertions, or scope.
- **Merge** — two cases verify the same primary behaviour and should become one case.
- **Remove** — the scenario is impossible, out of scope, obsolete, or fully duplicated.
- **Defer** — the coverage is useful but the expected business behaviour is not confirmed.
- **Reject** — the suggestion conflicts with confirmed scope/evidence or would introduce false expectations.

Do not automatically accept reviewer feedback as a requirement. A reviewer can identify a coverage gap without defining the expected behaviour.

## 3. Explain impact before rewriting

For unconfirmed feedback, provide a compact decision table:

| Feedback | Decision | Reason | Affected Cases | Required Clarification |
|---|---|---|---|---|

Explain duplication, scope, risk, and whether an exact expected result is available. Do not ask for clarification when available evidence already answers it.

## 4. Apply confirmed feedback

When the user confirms expected behaviour:

- update only related cases/groups;
- preserve unrelated approved content;
- retain existing IDs for updated cases;
- use the next unused ID for additions;
- remove or merge obsolete cases and update the manifest/count;
- update steps, Expected Result, and Expected Integration together so they remain aligned;
- re-run duplicate review.

If feedback changes a shared business rule, identify all cases that rely on the old rule, not only the case named by the reviewer.

## 5. Do not invent missing behaviour

Examples:

- A reviewer asks for Rental End Date coverage but the generation formula is absent: **Defer**, ask which source/calculation controls it, and do not add a guessed date.
- A reviewer suggests mixed batch validation and the user confirms per-invoice results plus valid-only reselection: **Add** a batch case with exact pass/fail and no-partial-export assertions.
- A reviewer identifies an impossible barcode scenario due to type-specific prefixes: **Remove** the case and record why it is impossible.

## 6. Final response shape

When feedback is still under review, show the decision and proposed change only. When the feedback is confirmed and the user says to do it, return the updated case(s) in the standard table without rewriting unaffected groups.
