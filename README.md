# INS LifeGuardian QA Workspace

This repository contains reusable QA instructions, product knowledge, requirement analysis, test cases, regression coverage, and confirmed decisions for INS LifeGuardian.

INS LifeGuardian is a healthcare, safety-monitoring, emergency-response, and client-support platform. QA analysis must consider client safety, security, data integrity, integrations, notifications, background processing, and cross-platform behaviour.

## Repository Purpose

This workspace helps Codex and QA team members:

* Analyse Jira tickets and requirements before writing test cases.
* Identify missing requirements, assumptions, conflicts, risks, and regression impact.
* Create practical UI, mobile, API, and regression test cases.
* Reuse confirmed product behaviour across related tickets.
* Prevent duplicate or conflicting test coverage.
* Maintain durable QA knowledge in the QA Second Brain.

## Codex Behaviour Standard

The Codex architecture uses progressive disclosure: `AGENTS.md` contains only always-on safety and workflow rules; the Analyst skill routes to task-specific references; QA Second Brain files are searched and opened only when relevant. This preserves ChatGPT-style QA behaviour while reducing repeated prompt context.

Detailed case generation normally uses:

- `.agents/skills/ins-lifeguardian-qa-analyst/references/test-case-style.md`
- `.agents/skills/ins-lifeguardian-qa-analyst/references/test-case-quality-gate.md`

Approved examples are loaded only for explicit comparison, format uncertainty, or drift review. They are not mandatory context for every test-case request.

Prompt-size drift is checked by `scripts/check_prompt_budget.py` and CI. Behaviour scenarios remain in `qa-evals/codex-behavior-evals.md`.

## How to Use This Repository

1. Start Codex from the repository root so `AGENTS.md` and project skills are discovered.
2. Supply the Jira ticket, screenshots, acceptance criteria, comments, API details, logs, or review feedback.
3. Let concise intake use the supplied evidence first.
4. Use `analytics` for deep ticket QA analysis without detailed test cases.
5. Use `write test cases for G1`, `review test cases`, and `next` for controlled case development.
6. Use `write test cases for all groups` only when a complete suite is required.
7. Use `Update test cases to Second Brain` with supplied Confluence cases to review, normalize, and directly update the Second Brain.
8. Use `write a bug` for a Jira defect. Use the dedicated Playwright API command chain for approved API automation; Web automation will be built separately later.
9. Search only relevant Second Brain files; run validators after stored changes.

## Canonical Workflow Commands

| Command | Purpose | Must not do |
|---|---|---|
| `analytics` | Any material ticket QA analysis | Detailed test-case rows or file writes |
| `write test cases for G#` | Write one approved group | Continue to another group unless requested |
| `write test cases for all groups` | Write the approved complete suite | Invent unresolved behaviour |
| `review test cases` | Apply the complete case quality gate | Rewrite unrelated cases |
| `Update test cases to Second Brain` | Retrieve supplied Confluence cases, review, normalize, and update relevant Second Brain files | Invent behaviour or bypass safety/validation gates |
| `write a bug` | Produce one Jira-ready bug | Claim unsupported root cause |
| `write API automation for <IDs>` | Implement approved cases in the API-only Playwright project | Create Web tests or invent contracts |
| `review API automation` | Apply the API automation quality gate | Change approved behavior to make code pass |
| `run API automation for <scope>` | Execute the narrowest API target | Use production or claim blocked execution passed |
| `debug API automation failure` | Classify from execution evidence | Assume every failure is a product defect |
| `fix API automation` | Fix proven automation defects | Weaken approved assertions |
| `update API automation mapping` | Synchronize automation status after evidence | Change manual case approval |

After a substantive result, Codex may show exactly one context-aware `Suggested next command:` line. It must not display a generic command menu or suggest storage before cases pass review.

Prompt examples are under `qa-knowledge/templates/`.

## Evidence Priority

Use evidence in this order when determining expected behaviour:

1. Current Jira ticket description and acceptance criteria
2. Confirmed Jira comments, decisions, screenshots, and attachments
3. Linked Confluence and API documentation
4. Relevant implementation, configuration, schemas, and automated tests
5. Related tickets and parent epics
6. Verified current product behaviour
7. Existing QA Second Brain knowledge
8. QA assumptions

Do not present assumptions as confirmed requirements.

When sources conflict, record the conflict and request clarification rather than silently selecting one behaviour. Use one decision per question with concrete selectable behaviour options, then record selected answers as Confirmed Decisions and update affected coverage.

## Supported Knowledge Statuses

Use only these Source Status values:

* `Confirmed`
* `QA Assumption`
* `Open Question`
* `Out of Scope`
* `Deprecated`
* `Conflict`

Definitions are maintained in:

`qa-knowledge/status-glossary.md`

Do not use unsupported statuses such as `Needs confirmation`.

## QA Second Brain

The QA Second Brain is located under:

`qa-knowledge/`

It stores reusable INS LifeGuardian QA knowledge.

### Main Files

* `qa-knowledge/index.md` — entry point and usage guidance
* `qa-knowledge/config.yml` — QA knowledge automation settings
* `qa-knowledge/status-glossary.md` — supported Source Status definitions
* `qa-knowledge/ticket-index.md` — ticket-to-knowledge file mapping

### Product Knowledge

* `qa-knowledge/product/product-map.md` — platform, module, and integration overview
* `qa-knowledge/product/modules/` — reusable knowledge by product module

### Requirement Knowledge

* `qa-knowledge/requirements/SMAR/` — SMAR ticket requirement analysis
* `qa-knowledge/requirements/MA/` — MA ticket requirement analysis

### Test Case Knowledge

* `qa-knowledge/test-cases/SMAR/` — approved SMAR test cases
* `qa-knowledge/test-cases/MA/` — approved MA test cases

### Automation Knowledge

* `qa-knowledge/automation/api-automation-map.md` — manual-case to Playwright API automation status
* `automation/api/mappings/automation-map.json` — executable mapping validated by the API project

### Regression and Decisions

* `qa-knowledge/regression/regression-map.md` — reusable regression impact and coverage
* `qa-knowledge/decisions/decision-log.md` — confirmed BA, Dev, QA, and product decisions

### Templates

* `qa-knowledge/templates/requirement-template.md`
* `qa-knowledge/templates/test-case-template.md`
* `qa-knowledge/templates/weekly-cleanup-report-template.md`
* `qa-knowledge/templates/analytics-prompt.md`
* `qa-knowledge/templates/write-test-case-group-prompt.md`
* `qa-knowledge/templates/review-test-cases-prompt.md`
* `qa-knowledge/templates/update-second-brain-prompt.md`
* `qa-knowledge/templates/write-bug-prompt.md`
* `qa-knowledge/templates/write-api-automation-prompt.md`
* `qa-knowledge/templates/review-api-automation-prompt.md`
* `qa-knowledge/templates/run-api-automation-prompt.md`
* `qa-knowledge/templates/debug-api-automation-prompt.md`
* `qa-knowledge/templates/update-api-automation-mapping-prompt.md`

The QA Second Brain is a reusable supporting knowledge base. Current Jira requirements, confirmed decisions, verified API contracts, current implementation evidence, and verified product behaviour take precedence.

## Codex Skills

### INS LifeGuardian QA Analyst

Location:

`.agents/skills/ins-lifeguardian-qa-analyst/`

Use this skill for:

* Jira and requirement review
* Requirement-gap analysis
* Risk and regression analysis
* API analysis
* UI, mobile, API, and regression test cases
* Bug reports
* QA feedback review

### INS LifeGuardian Playwright API Automation

Locations:

- `.agents/skills/ins-lifeguardian-playwright-api-automation/`
- `automation/api/`

Use this API-only skill and TypeScript framework to write, review, run, debug, fix, and map approved API automation. It uses standalone Playwright request contexts, safe non-production environments, isolated data, cleanup, exact traceability, and CI validation. Browser/Web automation is intentionally excluded and will be a separate future project.

### INS LifeGuardian QA Librarian

Location:

`.agents/skills/ins-lifeguardian-qa-librarian/`

Use this skill for:

* Saving approved requirements
* Saving approved test cases
* Updating product knowledge
* Updating confirmed decisions
* Updating regression coverage
* Detecting duplicate or conflicting QA knowledge
* Running QA knowledge cleanup

## Standard QA Workflow

Codex follows the requested response mode rather than always producing the full workflow.

Default concise intake:

1. Requirement Summary
2. Material QA Findings
3. Blocking or material Questions
4. Proposed Test Groups
5. Evidence limitations or assumptions only when present

Use `analytics` for a deeper review of applicable workflow, validation, data, API, permissions, privacy, integrations, jobs, notifications, audit, historical data, recovery, and regression. Empty or irrelevant sections are omitted.

Detailed cases are generated only when requested. One group is returned by default; a clear complete-suite request generates all requested groups without intermediate pauses.

## INS LifeGuardian Coverage

QA analysis may include:

### Platforms

* CP Desktop
* CP Web
* Portal Web
* Mobile SOS iOS and Android
* Mobile Carer iOS and Android
* Backend APIs
* Background services and jobs

### Modules

* Welfare Check
* Alerts and Restorals
* Emergency Alarm
* Notifications
* Tasks and Care Plan Tasks
* Device Setup and Checklist
* Service Requests and Work Orders
* Vital Signs and Thresholds
* Billing
* Reports
* Chat
* Roles and Permissions
* Assets and Devices
* Client File and Village inheritance
* Document Change Log

### Integrations

* FCM and push notifications
* SMS
* Email
* Twilio
* QuickBooks
* AWS and backend APIs
* Authentication and authorization
* Jobs and queues
* Alert delivery
* Notification logs
* Audit and operational logs

## QA Validation

After changing test cases or Second Brain knowledge, run:

```bash
python3 scripts/validate_qa_test_cases.py
python3 scripts/validate_qa_knowledge.py
python3 scripts/check_prompt_budget.py
python3 -m unittest discover -s tests -p "test_*.py"
```

Strict test-case validation intentionally fails while all stored case files are migration placeholders. CI always runs strict validation and must remain red until approved cases are migrated. For a local migration session only, opt in explicitly:

```bash
QA_MIGRATION_MODE=true
if [ "${QA_MIGRATION_MODE:-false}" = "true" ]; then
  python3 scripts/validate_qa_test_cases.py --allow-empty
else
  python3 scripts/validate_qa_test_cases.py
fi
```

Remove migration mode after approved cases have been stored. Do not treat stored cases or knowledge as approved when validation fails.

`.codex/environments/environment.toml` is autogenerated. The tracked file mirrors the strict-default setup, but the same conditional must remain configured in the Codex Environment Setup settings so regeneration does not restore permanent migration mode.

The test-case validator supports UI/Mobile, API, and Regression matrices, including group/ID consistency, semantic wording, step sequences, HTTP methods/statuses, and potential duplicate titles. The knowledge validator covers Knowledge Status, ticket-index integrity, orphan files, migration/completion gates, and decision/regression log requirements.

## Direct QA Second Brain Update

When approved or good test cases are supplied from Confluence, use:

```text
Update test cases to Second Brain
```

This single command authorizes the Librarian workflow. Codex retrieves the supplied page/content, infers the ticket, reviews the cases, applies safe non-behavioural corrections, updates relevant Second Brain files and indexes, preserves history, and runs preflight, backups, strict validators, and tests. No second approval phrase is required.

The preflight remains machine-enforced:

```bash
python3 scripts/second_brain_preflight.py \
  --approval-phrase "Update test cases to Second Brain" \
  --ticket SMAR-3000 \
  --proposed-file /tmp/SMAR-3000-reviewed.md \
  --create-ticket
```

Use `--create-ticket` only when targets do not exist. Use `--migration` when approved Confluence content replaces known migration placeholders. The preflight itself never writes files.

Safe corrections include formatting, IDs, High/Medium/Low priority, `Verify ` titles, reproducible steps, observable outcomes, traceability, duplicate consolidation, ranges, counts, and indexes. Codex must not invent or silently change product behaviour. Unsupported or conflicting items remain Could Not Verify, Open Question, Conflict, or GAP; unrelated supported updates continue.

## Repository Safety

Do not commit:

* API keys
* Passwords
* Access or refresh tokens
* Certificates or private keys
* Production client information
* Personal health information
* Unredacted logs containing sensitive data
* `.env` files
* Temporary exports or renders
* `.DS_Store`
* `__MACOSX/`
* Repository ZIP archives
* `.git/` content inside shared archives

Before sharing this repository, remove Git internals, operating-system metadata, secrets, production information, and temporary files. Create release archives from committed content:

```bash
git archive --format=zip --output=INS-LifeGuardian-clean.zip HEAD
unzip -l INS-LifeGuardian-clean.zip | grep -E '(^|/)(\.git|__MACOSX|\.DS_Store|\.cache|\.backups)'
```

The verification command should return no matches.
