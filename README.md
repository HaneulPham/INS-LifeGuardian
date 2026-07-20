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

The repository now uses an approved detailed-case pattern based on SMAR-2633. The behaviour architecture and evaluation workflow are documented in `docs/codex-qa-behavior.md`. Manual model-behaviour checks are available in `qa-evals/codex-behavior-evals.md`.

Detailed case generation must use:

- `.agents/skills/ins-lifeguardian-qa-analyst/references/test-case-style.md`
- `.agents/skills/ins-lifeguardian-qa-analyst/references/test-case-quality-gate.md`
- `.agents/skills/ins-lifeguardian-qa-analyst/references/examples/SMAR-2633-approved-test-case-pattern.md`
- `.agents/skills/ins-lifeguardian-qa-analyst/references/reviewer-feedback.md` for Rovo/BA/Dev/user feedback

## How to Use This Repository

1. Read `AGENTS.md` before performing INS LifeGuardian QA work.
2. Use the appropriate skill under `.agents/skills/`.
3. Review the relevant QA Second Brain files under `qa-knowledge/`.
4. Complete requirement, risk, integration, and regression analysis before generating detailed test cases.
5. Generate detailed test cases only when explicitly requested.
6. Write one test-case group at a time and wait for review before continuing.
7. Run the QA validator after creating or updating stored test cases.
8. Update the QA Second Brain only through the approved QA librarian workflow.

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

When sources conflict, record the conflict and request clarification rather than silently selecting one behaviour.

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

### Regression and Decisions

* `qa-knowledge/regression/regression-map.md` — reusable regression impact and coverage
* `qa-knowledge/decisions/decision-log.md` — confirmed BA, Dev, QA, and product decisions

### Templates

* `qa-knowledge/templates/requirement-template.md`
* `qa-knowledge/templates/test-case-template.md`
* `qa-knowledge/templates/weekly-cleanup-report-template.md`

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

For requirement, Jira, BA, Dev, screenshot, or API review:

1. Requirement Analysis
2. Scope
3. Missing Requirements and Gaps
4. Risk Analysis
5. Backend and Integration Impact
6. Required Validations
7. Questions grouped as Critical, Important, and Optional
8. Proposed Test Case Coverage

Do not generate detailed test cases unless the user explicitly requests a group.

When detailed cases are requested:

1. Check existing requirements and test cases.
2. Avoid duplicate coverage.
3. Write only the requested group.
4. Stop and wait for review.
5. Continue only after the user says `next`, `next group`, or `go ahead`.

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

## QA Second Brain Approval

When the reviewed analysis and cases are ready to store, use:

```text
Approve and Update the QA Second Brain for ticket <Ticket ID>
```

Codex will apply the behaviour defined in:

* `AGENTS.md`
* `.agents/skills/ins-lifeguardian-qa-librarian/SKILL.md`
* `qa-knowledge/config.yml`

Before an automatic write, the Librarian runs `scripts/second_brain_preflight.py`. It enforces the configured approval, ticket, clean-worktree, migration, conflict, sensitive-content, backup-ignore, and target-file gates.

For a genuinely new approved ticket, use the explicit read-only creation gate:

```bash
python3 scripts/second_brain_preflight.py \
  --approval-phrase "Approve and Update the QA Second Brain for ticket SMAR-3000" \
  --ticket SMAR-3000 \
  --proposed-file /tmp/SMAR-3000-approved.md \
  --create-ticket
```

After it passes, the Librarian creates the requirement and test-case files from the approved templates, adds the ticket index row, and runs both strict validators. The preflight itself never creates files.

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
