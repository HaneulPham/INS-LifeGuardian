---
name: ins-lifeguardian-qa-librarian
description: Maintain the INS LifeGuardian QA Second Brain, including approved requirements and test cases, product knowledge, decisions, regression coverage, indexes, migrations, and weekly cleanup reports.
---

# INS LifeGuardian QA Librarian

Maintain `qa-knowledge/` as concise, searchable, evidence-backed product knowledge. Store only supported requirements, rules, cases, decisions, and regression relationships. Never invent behaviour or expose credentials, production secrets, patient/client information, or private health information.

## Direct command and evidence review

`Update test cases to Second Brain` is direct authorization to retrieve, review, normalize, and store the supplied Confluence test cases. Do not require another approval phrase. Infer the ticket from the page, case IDs, or active context; ask only if it cannot be identified safely.

Before applying an update, read only relevant evidence:

1. `qa-knowledge/config.yml`
2. `qa-knowledge/index.md`, `ticket-index.md`, and `status-glossary.md`
3. The related module, requirement, and test-case files
4. `qa-knowledge/decisions/decision-log.md`
5. `qa-knowledge/regression/regression-map.md`
6. The approved conversation evidence and any stronger Jira, Confluence, repository, or runtime evidence

Check for duplicate and conflicting behaviour or cases. Do not duplicate coverage for wording, data, or navigation differences alone. Keep separate cases only for distinct rules, validation, roles, platforms, integrations, failure modes, boundaries, or regression risks. Report what was merged, removed, or retained and why.

## Source Status

Use only **Confirmed**, **QA Assumption**, **Open Question**, **Out of Scope**, **Deprecated**, and **Conflict** as defined by the glossary. Every requirement and module file must contain the canonical `Knowledge Status` table with source/evidence and `Last Updated`. Never promote an assumption or question without confirming evidence, and never overwrite a Confirmed conflict silently.

## Direct execution and auto-apply gate

The workflow begins when the user says `Update test cases to Second Brain` and supplies Confluence content or a retrievable page. Retrieve it using the configured Atlassian tools, sanitize a local proposed-content file, and review it before any write.

If `automation.auto_apply_second_brain_updates` is false, prepare the reviewed proposal and report that automatic writes are disabled. If true, run preflight before backups or writes:

```bash
python3 scripts/second_brain_preflight.py \
  --approval-phrase "Update test cases to Second Brain" \
  --ticket <inferred-ticket-id> \
  --proposed-file <sanitized-reviewed-content>
```

Use `--migration` only when the user explicitly requests migration and the approved source requirement/case content is available. A normal approval must stop on migration placeholders.

For a new ticket whose target files do not exist, run the same command with `--create-ticket`. This mode requires sanitized proposed content, rejects an existing target or ticket-index row, verifies the base directories and approved templates, and remains read-only. Without `--create-ticket`, missing targets must fail.

The preflight enforces the direct command phrase, ticket format, clean worktree, target/create mode, sensitive-content block, ignored backup destination, and enabled flags. Preserve evidence-backed Conflict/GAP records and keep the ticket incomplete while updating unrelated valid content. When it fails, make no Second Brain changes. Do not stash, discard, stage, commit, overwrite unrelated work, bypass strict checks with `--allow-empty`, or echo sensitive values.

## Review and normalization before storage

Review supplied cases against the complete case quality gate. Safe corrections may include formatting, grammar, IDs, group ranges, High/Medium/Low priorities, `Verify ` titles, reproducible steps, observable outcomes, traceability formatting, duplicate consolidation, indexes, and counts. Do not silently change product behaviour, contracts, roles, messages, status codes, integrations, or expected states.

For each case classify Add, Update, Merge, Remove, Retain, Defer, or Could Not Verify. Before Merge/Remove, prove that no unique requirement, risk, role, platform, boundary, integration state, failure mode, evidence type, or outcome is lost. Preserve unresolved conflicts and update unaffected valid cases.

## Safe update transaction

After preflight passes:

1. Respect `update_ticket_index`, `update_regression_map`, and `update_decision_log`; a false flag prohibits that target.
2. If `create_backup` is true, create a timestamped backup under the configured ignored directory, preserving relative paths.
3. For `--create-ticket`, safely create the ticket-family subdirectories when absent, instantiate requirement and test-case files from `qa-knowledge/templates/`, replace template ticket placeholders, and add exactly one ticket-index row.
4. Update only the approved requirement, test cases, applicable module knowledge, and enabled index/log targets.
5. Apply Source Status labels and re-check duplicates/conflicts.
6. If enabled, run strict validation:

```bash
python3 scripts/validate_qa_test_cases.py
python3 scripts/validate_qa_knowledge.py
```

7. If either validator fails, restore the backup and report the failure. Do not mark the update approved or complete.

## Ticket completion gate

Mark a ticket `Completed` only when:

- Requirement and test-case migration placeholders are removed.
- All approved groups are stored as actual valid rows.
- Strict test-case and knowledge validation pass without `--allow-empty`.
- Indexed requirement and case files exist.
- The requirement has a valid Knowledge Status table.
- Applicable confirmed decisions and regression impacts are logged, or the requirement explicitly says `None` for non-applicable sections.

## Direct-update output

After a successful update, report:

- Updated Files
- New Confirmed Knowledge
- Test Cases Saved
- Regression Map Updates
- Open Questions
- Duplicates or Conflicts Found
- Validator results

## Weekly cleanup

When the user says `Run weekly QA knowledge cleanup`, review the full Second Brain and prepare a report only. Check duplicate requirements/cases, conflicts, stale assumptions, open questions, orphaned requirements/cases, missing statuses or index entries, regression gaps, vague expectations, invalid IDs, and invalid priorities.

Do not edit or delete files automatically. Return Summary, Issues Found, Recommended Fixes, Files Impacted, Safe Auto-Fixes, and Items Requiring User Approval, then wait.
