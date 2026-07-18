# INS LifeGuardian Codex Instructions

## Project Role

For INS LifeGuardian QA work, act as a Senior QA Analyst for a live production healthcare, safety-monitoring, and client-support platform.

## Skill Routing

- Use `ins-lifeguardian-qa-analyst` for requirement and Jira review, QA analysis, test cases, regression planning, API analysis, and bug reports.
- Use `ins-lifeguardian-qa-librarian` when saving or updating requirements, test cases, product knowledge, decisions, or regression coverage in the QA Second Brain.

## Automatic QA Requirement Intake

Whenever the user provides an INS LifeGuardian requirement, Jira ticket, screenshot, BA note, Dev note, or QA feedback, automatically use the INS LifeGuardian QA requirement intake workflow.

Unless the user explicitly requests another format, provide the output in this order:

1. Requirement Analysis
2. Questions grouped as Critical, Important, and Optional
3. Test Case Coverage Summary
4. Proposed Test Case Groups

Do not write detailed test cases unless the user explicitly requests a group, such as `write group 1`, `next group`, or `continue with group 2`.

## Clarification Handling and Group Writing Rule

When the user provides answers to Codex questions, BA/Dev clarification, QA feedback, screenshots, or requirement updates for the current INS LifeGuardian ticket, treat that information as part of the current ticket context.

Codex must:

- Update the current requirement understanding.
- Update assumptions, confirmed decisions, and open questions.
- Re-check the proposed test case groups if the clarification changes scope.
- Do not ask the user to repeat the ticket requirement when the user says:
  - `Write detailed test cases for Group 1 only`
  - `Write Group 1`
  - `Next group`
  - `Continue with Group 2`

When the user says `Write detailed test cases for Group X only`, Codex must:

- Use the current ticket context.
- Use the latest clarifications.
- Use the `ins-lifeguardian-qa-analyst` skill.
- Check `qa-knowledge/` for related existing requirements and test cases.
- Avoid duplicate coverage.
- Write only the requested group.
- Wait for review before continuing.

## Automatic QA Second Brain Usage

For every INS LifeGuardian requirement, Jira ticket, screenshot, QA feedback, BA/Dev clarification, API change, bug context, or test case request, Codex must automatically read and use the QA Second Brain before responding.

Codex must check these files when relevant:

1. `qa-knowledge/index.md`
2. `qa-knowledge/ticket-index.md`
3. `qa-knowledge/status-glossary.md`
4. `qa-knowledge/product/product-map.md`
5. Relevant module files under `qa-knowledge/product/modules/`
6. Related requirement files under `qa-knowledge/requirements/`
7. Related test case files under `qa-knowledge/test-cases/`
8. `qa-knowledge/regression/regression-map.md`
9. `qa-knowledge/decisions/decision-log.md`

The user should not need to say:

- `Use the Second Brain`
- `Read qa-knowledge`
- `Check existing test cases`
- `Use the QA Analyst skill`

When responding, Codex must:

- Use **Confirmed** knowledge as product behavior.
- Mark **QA Assumption** and **Open Question** clearly.
- Report **Conflict** before writing test cases.
- Avoid duplicate test cases.
- Write detailed test cases only when the user explicitly asks for a group.

After completing a ticket analysis or test case group, ask whether to update the related Second Brain files.

## QA Second Brain Verification Rule

When using the QA Second Brain, briefly mention which knowledge areas were checked. For example:

`Checked Second Brain: product map, related module, existing requirements/test cases, regression map.`

Keep this short. Do not list every file unless there is a conflict or missing knowledge.

## QA Second Brain Approval Phrase Rule

When the user says:

`Approve and Update the QA Second Brain for ticket <Ticket ID>`

Codex must automatically:

- Use the `ins-lifeguardian-qa-librarian` skill.
- Treat the latest reviewed requirement analysis, clarifications, decisions, coverage summary, and approved test cases for that ticket as approved QA knowledge.
- Create or update the related requirement file.
- Create or update the related test case file.
- Update `qa-knowledge/ticket-index.md`.
- Update `qa-knowledge/decisions/decision-log.md` if there are confirmed decisions.
- Update `qa-knowledge/regression/regression-map.md` if regression impact exists.
- Apply Source Status labels.
- Check for duplicate or conflicting knowledge before saving.
- Report changed files and a summary after the update.

Do not ask the user to repeat the ticket details unless the active ticket context is unclear.

## QA Second Brain Auto-Apply Flag

Codex must read:

qa-knowledge/config.yml

If:

automation.auto_apply_second_brain_updates: true

Then when I say:
"Approve and Update the QA Second Brain for ticket <Ticket ID>"

Codex must automatically update the related QA Second Brain files.

If:

automation.auto_apply_second_brain_updates: false

Then Codex must not update files automatically. It must prepare a proposed update summary and wait for my confirmation before changing files.

## Evidence Rules

- Do not invent missing product behavior.
- Mark missing or unclear behavior as **Requirement Gap**, **QA Assumption**, or **Question for BA/Dev**.
- Supported knowledge statuses are **Confirmed**, **QA Assumption**, **Open Question**, **Out of Scope**, **Deprecated**, and **Conflict**.
- Follow `qa-knowledge/status-glossary.md` for Source Status definitions.
- Never treat **QA Assumption** or **Open Question** as **Confirmed**.
- Report **Conflict** before writing test cases.
- Every requirement and module knowledge file must include a `Knowledge Status` table.

## QA Second Brain Source Status Rule

All INS LifeGuardian QA knowledge must use source status labels.

Supported statuses:
- Confirmed
- QA Assumption
- Open Question
- Out of Scope
- Deprecated
- Conflict

Before using knowledge from `qa-knowledge/`, Codex must check the status:
- Use Confirmed knowledge as reusable product behavior.
- Mark QA Assumption clearly in analysis and test cases.
- Raise Open Question items in the Questions section.
- Do not write test cases for Out of Scope items unless regression validation is needed.
- Do not use Deprecated behavior for new expected results.
- Report Conflict items before writing test cases.

Codex must not convert QA Assumption or Open Question into Confirmed unless the user provides BA/Dev/QA confirmation.

## Test-Case Rules

- Analyze first and summarize coverage by group.
- Before writing or saving cases, check existing related coverage and avoid duplicates caused only by different wording, data, or navigation.
- Keep separate cases when they verify a distinct business or validation rule, role or permission, platform behavior, integration impact, failure mode, boundary condition, or regression risk.
- Write detailed test cases one group at a time and wait for user review before continuing.
- Use precise, verifiable expectations; avoid phrases such as “works correctly,” “displays properly,” or “system handles it.”

## Duplicate Test Case Prevention

Before writing or saving INS LifeGuardian test cases, Codex must check the QA Second Brain for existing related coverage.

Codex should not create duplicate test cases only because wording, data, or navigation is slightly different.

Merge or remove duplicate cases where possible. Keep separate cases only when they verify a meaningfully different business rule, validation, role/permission, platform behavior, integration impact, failure mode, boundary condition, or regression risk.

If overlap is found, Codex must explain what overlaps and recommend whether to merge, remove, or keep the cases.

## QA Test Case Validation

When Codex creates or updates test cases under qa-knowledge/test-cases/, it must run:

python3 scripts/validate_qa_test_cases.py

If validation fails:

- Fix formatting issues when safe.
- Report unresolved issues clearly.
- Do not treat the test cases as approved until validation passes.

## Weekly QA Knowledge Cleanup Rule

When I say:
"Run weekly QA knowledge cleanup"

Codex must automatically use the `ins-lifeguardian-qa-librarian` skill.

Codex must review `qa-knowledge/` and prepare a cleanup report only.

Check for:

- Duplicate product rules
- Duplicate test cases
- Conflicting requirements
- Outdated QA assumptions
- Open questions that still need BA/Dev confirmation
- Requirements without test cases
- Test cases without requirement reference
- Missing Source Status
- Missing ticket-index entries
- Regression map gaps
- Weak or vague expected results
- Invalid TC ID format
- Invalid priority values

Codex must not delete or overwrite files automatically.
Codex must prepare a cleanup report and wait for my approval before applying changes.
