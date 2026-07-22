# INS LifeGuardian Codex Behaviour Evals

Use these scenarios after changing `AGENTS.md`, the QA Analyst skill, templates, or validators. Run each prompt in a new Codex chat from the repository root and score the response against the checklist.

## Eval 1 — Requirement intake, no premature cases

### Prompt

```text
Here is ticket SMAR-9999: Add a new DVA invoice date rule. Pending invoices can edit the date. The date must be the first day of a month.
```

### Pass criteria

- Activates requirement review/intake without asking what output is wanted.
- Summarizes intent, gaps, risks, backend/integration impact, questions, and proposed groups.
- Does not write detailed test-case rows.
- Labels unknown status rules and error text as open questions rather than assumptions.

## Eval 2 — Group 1 full executable workflow

### Prompt

```text
Write detailed test cases for Group 1 only.
```

Use after Eval 1 in the same chat.

### Pass criteria

- Outputs Group 1 only.
- Every UI/API Title is plain text beginning with `Verify `.
- First case includes platform login/open, exact menu path, locating the prepared record, confirming source data, performing the action, reviewing the result, and downstream validation/export when applicable.
- Expected Result and Expected Integration use `Verify after step #N` markers.
- Exact values, persistence, duplicate prevention, and no unintended integrations are stated.
- Stops for review instead of writing Group 2.

## Eval 3 — `next` continuity

### Prompt

```text
next
```

### Pass criteria

- Writes the next not-yet-reviewed group only.
- Does not repeat Group 1.
- Preserves approved IDs and decisions.
- Does not ask the user to repeat the ticket.

## Eval 4 — Reviewer feedback with incomplete business behaviour

### Prompt

```text
Rovo says to add the expected Rental End Date to the generation case, but the ticket does not define how Rental End Date is generated. Review this feedback.
```

### Pass criteria

- Classifies the item as Defer, not Add with a guessed date.
- Explains why the exact generation source/formula is required.
- Identifies the affected group/case.
- Does not rewrite unrelated cases.

## Eval 5 — Confirmed reviewer feedback

### Prompt

```text
Batch validation supports multiple invoices. Validation returns individual results. The user must clear the mixed selection and create a new selection containing only valid invoices before export. Add the related case.
```

### Pass criteria

- Adds one distinct high-priority batch case using the next unused ID.
- Verifies separate pass/fail results, exact IVL027 message, no partial export from the mixed selection, valid-only reselection, one export for the valid invoice, and no XML/queue/submission for the invalid invoice.
- Returns only the affected case/group, preserving unrelated content.

## Eval 6 — Impossible or duplicate scenario

### Prompt

```text
A reviewer asks for a test where two asset types have the same barcode, but confirmed product rules give every asset type a unique prefix so the scenario cannot occur. Review the feedback.
```

### Pass criteria

- Classifies the case as Remove or Reject.
- Explains why it is impossible from confirmed product rules.
- Does not retain the case as a generic negative test.

## Eval 7 — Explicit complete-suite override

### Prompt

```text
Write all approved test-case groups for the active ticket in one response. Do not stop between groups.
```

### Pass criteria

- Produces all requested groups in plan order without asking for approval between groups.
- Applies the full detailed-case quality gate to every group.
- Preserves approved IDs and does not duplicate coverage.

## Eval 8 — Internal rule without observable evidence

### Prompt

```text
Add a test case proving which internal dialler fallback object was selected, but the UI shows only that a call started and no call/log evidence is available.
```

### Pass criteria

- Does not present the internal-object assertion as an executable test.
- Labels the scenario Requires Test Instrumentation.
- Names practical evidence such as the called number, approved call log, or correlation-linked backend log.
- Does not claim an implementation result without evidence.

## Scoring

- 2 points per fully met criterion.
- 1 point for partially met.
- 0 points for missed or contradicted.
- Target: at least 90%, with zero failures for premature case generation, invented expected behaviour, wrong group continuation, or duplicate/renumbered approved IDs.
