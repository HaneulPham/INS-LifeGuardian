---
name: ins-lifeguardian-qa-librarian
description: Use this skill to update, organize, summarize, refactor, or maintain the INS LifeGuardian QA Second Brain. Trigger when the user asks to remember requirements, save test cases, update product knowledge, update the regression map, summarize completed tickets, avoid duplicate future test cases, or says "Approve and Update the QA Second Brain for ticket <Ticket ID>".
---

# INS LifeGuardian QA Librarian Skill

## Purpose

Maintain the INS LifeGuardian QA Second Brain as a clean, searchable, and reliable product knowledge base.

The Second Brain is located at:

`qa-knowledge/`

## Main Responsibilities

When updating the Second Brain:
- Store confirmed requirements.
- Store confirmed business rules.
- Store confirmed test cases.
- Store confirmed BA/Dev/QA decisions.
- Store regression risks.
- Store module behavior.
- Avoid duplicate knowledge.
- Do not invent missing behavior.
- Mark uncertain behavior as QA assumption or open question.
- Keep content concise and easy for Codex to reuse later.

## Update Rules

Before updating any file:
1. Read `qa-knowledge/index.md`.
2. Read related module file under `qa-knowledge/product/modules/`.
3. Read existing ticket requirement file if it exists.
4. Read existing test case file if it exists.
5. Read `qa-knowledge/decisions/decision-log.md`.
6. Check for duplicate or conflicting behavior.

After updating:
- Summarize what changed.
- List files changed.
- List open questions.
- List possible conflicts.
- Unless the user used the approval phrase, ask the user to review before treating new behavior as confirmed.

## Duplicate Knowledge and Test Case Prevention Rule

Before saving new requirements or test cases into the QA Second Brain:

1. Check whether the same behavior already exists in:
   - `qa-knowledge/ticket-index.md`
   - Related requirement files
   - Related test case files
   - Related module files
   - `qa-knowledge/decisions/decision-log.md`
   - `qa-knowledge/regression/regression-map.md`

2. If duplicate test case coverage is found:
   - Do not save the duplicate as a new test case.
   - Do not treat wording, data, or navigation differences alone as unique coverage.
   - Recommend merging it into the existing test case.
   - Preserve only unique validation, integration, permission, data, or regression checks.

3. If similar but not duplicate:
   - Keep both only for a different business rule, validation, role/permission, platform behavior, integration impact, failure mode, boundary condition, or regression risk.
   - Add a note explaining the difference.
   - If coverage overlaps, explain what overlaps and recommend whether to merge, remove, or keep both.

4. If conflicting knowledge is found:
   - Mark the item as `Conflict`.
   - Report the conflict before updating the Second Brain.
   - Do not overwrite confirmed behavior without user confirmation.

After updating the Second Brain, report:
- Duplicate items found
- Items merged
- Items removed
- Items kept separately and why

## Source Status Rule

Use `qa-knowledge/status-glossary.md` and these statuses only: **Confirmed**, **QA Assumption**, **Open Question**, **Out of Scope**, **Deprecated**, and **Conflict**.

- Do not treat **QA Assumption** or **Open Question** as **Confirmed**.
- Include a `Knowledge Status` table in every requirement and module knowledge file.
- Report **Conflict** before replacing confirmed knowledge or saving conflicting test-case guidance.
- Preserve the source or evidence for each status assignment.

## Source Status Maintenance Rule

When updating the Second Brain:
- Add every new requirement, rule, or decision to a Knowledge Status table.
- Assign one status: Confirmed, QA Assumption, Open Question, Out of Scope, Deprecated, or Conflict.
- Add source: Ticket, BA feedback, Dev feedback, QA feedback, Screenshot, Existing Product, API evidence, DB evidence, or Test Evidence.
- Add Last Updated date.
- Add short notes explaining why the status was selected.

Do not mark a rule as Confirmed unless it is clearly supported by ticket text, BA/Dev/QA feedback, screenshots, implementation evidence, API/DB evidence, or verified testing evidence.

## Auto-Apply Flag Rule

Before updating the QA Second Brain, check:

qa-knowledge/config.yml

If `automation.auto_apply_second_brain_updates` is true:
- Update the QA Second Brain files automatically after the approval phrase.
- Apply Source Status.
- Check duplicates/conflicts.
- Run validation if configured.
- Report changed files.

If `automation.auto_apply_second_brain_updates` is false:
- Do not update files yet.
- Prepare the proposed changes.
- List files that would be changed.
- Wait for user confirmation.

## Approval Phrase Workflow

When the user says:

`Approve and Update the QA Second Brain for ticket <Ticket ID>`

Perform this workflow:

1. Identify the active ticket ID.
2. Use the latest conversation context for:
   - Requirement summary
   - Confirmed scope
   - Out of scope
   - Clarifications
   - Confirmed decisions
   - Open questions
   - QA assumptions
   - Approved test case groups
   - Regression impacts
3. Update or create the requirement file:
   - `qa-knowledge/requirements/SMAR/<Ticket ID>.md` for SMAR tickets
   - `qa-knowledge/requirements/MA/<Ticket ID>.md` for MA tickets
4. Update or create the test case file:
   - `qa-knowledge/test-cases/SMAR/<Ticket ID>.md` for SMAR tickets
   - `qa-knowledge/test-cases/MA/<Ticket ID>.md` for MA tickets
5. Update:
   - `qa-knowledge/ticket-index.md`
   - `qa-knowledge/decisions/decision-log.md` when confirmed decisions exist
   - `qa-knowledge/regression/regression-map.md` when regression impact exists
   - Relevant module file under `qa-knowledge/product/modules/` when product behavior is confirmed
6. Apply Source Status:
   - **Confirmed**
   - **QA Assumption**
   - **Open Question**
   - **Out of Scope**
   - **Deprecated**
   - **Conflict**
7. Check for duplicates and conflicts:
   - Do not duplicate existing requirement or test case knowledge.
   - Merge related coverage where appropriate.
   - Mark conflicts clearly and ask for confirmation before overwriting confirmed behavior.
8. Include in the final response:
   - Updated Files
   - New Confirmed Knowledge
   - Test Cases Saved
   - Regression Map Updates
   - Open Questions
   - Duplicates or Conflicts Found

## Second Brain Test Case Validation Rule

Before saving approved test cases into the QA Second Brain, run:

python3 scripts/validate_qa_test_cases.py

If validation fails:

- Do not mark the update as complete.
- Fix safe formatting issues.
- Report duplicate TC IDs, invalid priorities, missing Expected Result, or missing Expected Integration.

## Weekly QA Knowledge Cleanup Workflow

When the user says:
"Run weekly QA knowledge cleanup"

Perform this workflow:

1. Read:
   - qa-knowledge/index.md
   - qa-knowledge/ticket-index.md
   - qa-knowledge/status-glossary.md
   - qa-knowledge/product/product-map.md
   - qa-knowledge/product/modules/
   - qa-knowledge/requirements/
   - qa-knowledge/test-cases/
   - qa-knowledge/regression/regression-map.md
   - qa-knowledge/decisions/decision-log.md

2. Check for:
   - Duplicate requirements
   - Duplicate test cases
   - Conflicting product rules
   - Open questions
   - QA assumptions older than current confirmed behavior
   - Missing Source Status
   - Missing related ticket links
   - Requirements without test cases
   - Test cases without requirement reference
   - Regression map gaps
   - Invalid TC ID format
   - Invalid priority values
   - Vague expected results or expected integrations

3. Do not change files immediately.

4. Create a cleanup report with:
   - Summary
   - Issues Found
   - Recommended Fixes
   - Files Impacted
   - Safe Auto-Fixes
   - Items Requiring User Approval
   - Open Questions

5. Wait for user approval before updating files.

## Do Not Store

Do not store:
- Real client/patient names
- Real phone numbers
- Real addresses
- API tokens
- Passwords
- Production secrets
- Private health information
- Any sensitive data not needed for QA reuse

Use sanitized QA data only.

## Standard Output After Update

Respond with:

1. Updated Files
2. New Confirmed Knowledge
3. Updated Test Case Knowledge
4. Regression Map Updates
5. Open Questions
6. Conflicts or Duplicates Found
