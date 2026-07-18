#!/usr/bin/env python3
"""Apply evidence-first QA analytics improvements to INS-LifeGuardian.

Usage:
    python3 apply_evidence_first_analytics.py /path/to/INS-LifeGuardian

The script:
- creates timestamped backups of edited files;
- adds an evidence hierarchy to AGENTS.md;
- adds an evidence-acquisition gate and evidence-reporting rule to the QA analyst skill;
- strengthens Default Requirement Intake and Requirement Review Mode;
- adds an approved SMAR-2650 analysis-pattern reference;
- adds a reusable requirement-review prompt template.

It is idempotent: existing evidence-first sections are not duplicated.
"""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path


AGENTS_EVIDENCE_SECTION = r'''## Evidence-First QA Analysis Rule

Before producing a requirement review, API review, risk analysis, regression plan, or test coverage proposal, Codex must inspect the strongest available evidence in this order:

1. Current Jira ticket description and acceptance criteria.
2. Confirmed Jira comments, decisions, history, screenshots, and attachments.
3. Linked Confluence pages, API contracts, and technical documentation.
4. Parent epic and directly related tickets.
5. Relevant repository implementation, configuration, schemas, handlers, tests, and generated infrastructure.
6. Verified current product behaviour and test evidence.
7. Relevant QA Second Brain knowledge under `qa-knowledge/`.
8. Clearly labelled QA assumptions.

Codex must not rely only on the Jira summary or only on the QA Second Brain when stronger or newer evidence is available.

Before writing the Requirement Summary, Codex must either:

- complete the available evidence review; or
- state which private or repository evidence could not be accessed.

When sources conflict, Codex must:

- identify each conflicting source;
- explain the behavioural difference;
- apply the evidence priority above;
- record an **Open Question** or **Conflict** when the intended behaviour remains unresolved;
- avoid silently choosing one expected result.

For repository evidence, search exact entities such as ticket IDs, endpoint paths, HTTP methods, function names, handler names, YAML keys, API models, queue names, FCM actions, notification types, database fields, and error messages.

Every completed requirement review must include:

- **Evidence Reviewed**
- **Could Not Verify**
- **QA Assumptions**

'''

SKILL_EVIDENCE_SECTIONS = r'''## Evidence Acquisition Gate

Do not begin the Requirement Summary until the available evidence has been inspected or the unavailable evidence has been explicitly recorded.

### Evidence order

Use this order:

1. Current Jira ticket description and acceptance criteria.
2. Confirmed ticket comments, decisions, changelog/history, screenshots, and attachments.
3. Linked Confluence pages, API contracts, architecture notes, and technical documentation.
4. Parent epic and directly related tickets.
5. Relevant source code, `serverless.yml`, infrastructure configuration, handlers, contracts, schemas, automated tests, and generated deployment artifacts.
6. Verified current product behaviour and QA execution evidence.
7. Relevant files under `qa-knowledge/`.
8. Clearly labelled QA assumptions.

### Jira or ticket workflow

When a Jira URL or ticket key is available and the required connector/tool is available:

1. Fetch the complete ticket, not only the summary.
2. Read acceptance criteria, comments, relevant history, screenshots, and attachments.
3. Inspect the parent epic and directly related tickets when they affect intent, security, migration, or compatibility.
4. Open linked Confluence/API documentation.
5. Compare the ticket with repository evidence and QA Second Brain knowledge.

If Jira, Confluence, attachments, or private documents cannot be accessed, state this under **Could Not Verify**. Do not replace unavailable private evidence with generic web assumptions.

### Repository investigation

Search exact identifiers before making implementation claims. Examples:

```bash
rg -n "<TICKET-ID>" .
rg -n "<endpoint-path>|<function-name>|<handler-name>" .
rg -n "authorizer:|private:|http:|events:" path/to/serverless.yml
rg -n "<request-field>|<response-field>|<enum-value>" src tests docs
```

Inspect applicable evidence such as:

- Function and handler declarations
- Endpoint methods and paths
- Authentication and permission configuration
- Request/response contracts
- Database keys and audit fields
- Jobs, queues, schedules, retries, and dead-letter handling
- FCM, SMS, email, Twilio, and notification actions
- Reports, exports, and billing integrations
- Existing tests and generated CloudFormation/deployment output

Do not claim root cause, active consumer usage, persistence behaviour, or authorization behaviour without evidence.

### Conflict handling

When sources disagree:

- Name the sources.
- Describe the conflict precisely.
- Identify which source has higher priority.
- Mark unresolved behaviour as **Conflict** or **Open Question**.
- Do not write a confirmed expected result for the unresolved behaviour.

## Evidence Reporting Rule

Finish each requirement or API review with:

### Evidence Reviewed

List the ticket, documentation, source/configuration files, related tickets, tests, commands, and runtime evidence actually inspected.

### Could Not Verify

List missing or inaccessible evidence that could materially change the analysis.

### QA Assumptions

List only assumptions actually used. If none were used, write `None`.

Keep evidence reporting concise but specific. Reference exact file paths, endpoint paths, function names, configuration keys, or ticket/page names where available.

'''

DEFAULT_INTAKE = r'''## Default Requirement Intake Rule

When the user provides an INS LifeGuardian requirement, Jira ticket, screenshot, BA note, Dev note, QA feedback, or API change, use the Evidence Acquisition Gate first and respond in this order:

1. Requirement Summary
   - Current defect, limitation, or requested change
   - Expected implementation or business behaviour
   - Main affected components
   - Behaviour that must remain unchanged
2. Scope
   - In Scope
   - Out of Scope
   - Conditional Scope / Needs Confirmation
3. Missing Requirements and Gaps
   - Critical
   - Important
   - Optional
4. Risk Analysis
5. Backend and Integration Impact
6. Required Validations
7. Questions grouped as Critical, Important, and Optional
8. Proposed Test Coverage
9. Evidence Reviewed / Could Not Verify / QA Assumptions

Do not write detailed test cases until the user requests a specific group.

'''

REQUIREMENT_REVIEW_MODE = r'''## Requirement Review Mode

For requirement, story, ticket, BA, Dev, security-remediation, or technical-configuration review, return these sections in order:

### 1. Requirement Summary

Explain:

- Current defect, limitation, or business problem
- Expected implementation or intended behaviour
- Main affected components and consumers
- Existing behaviour that must remain unchanged

Interpret the intent; do not merely rewrite the ticket.

### 2. Scope

Separate:

- In Scope
- Out of Scope
- Conditional Scope / Needs Confirmation

Do not expand the ticket silently. Label recommendations and potential follow-up work.

### 3. Missing Requirements and Gaps

Group gaps as:

- Critical
- Important
- Optional

Consider exact workflow or endpoint, authentication, permissions, fields, validation, errors, duplicates, idempotency, retries, persistence, migration, compatibility, cross-platform behaviour, logging, audit, deployment, rollback, and integration ownership.

Explain why each meaningful gap matters to testing or release safety.

### 4. Risk Analysis

Consider applicable risks:

- Client health or safety
- Security and unauthorized access
- Cross-client or cross-tenant data leakage
- Data corruption, loss, false persistence, or duplicate processing
- Missed, delayed, duplicate, or incorrect alerts and notifications
- Mobile/Web/Desktop inconsistency
- Job, queue, retry, timing, and recovery behaviour
- Deployment and rollback
- Backward compatibility and active consumers
- Reports, billing, and exports
- Logging and observability

For every meaningful risk, state the failure consequence. Avoid generic statements such as `regression may occur`.

### 5. Backend and Integration Impact

Review applicable impact on:

- API Gateway and backend APIs
- Lambda/services and handlers
- Authentication and authorization
- Database and persistence
- Jobs, queues, schedules, retries, and DLQs
- CP Desktop, CP Web, Portal Web, SOS, and Carer apps
- FCM, SMS, email, Twilio, and alert delivery
- Reports, QuickBooks, and billing
- Audit logs, notification logs, CloudWatch, history, and Document Change Log

Explicitly state when no downstream process should run.

### 6. Required Validations

List observable validations for applicable areas:

- Static configuration and source review
- Build and packaging
- Generated infrastructure
- Deployment and rollback
- Runtime positive behaviour
- Authentication and authorization
- Negative and failure paths
- Data persistence and no-false-persistence
- Logs, audit, and correlation
- Cross-platform and consumer regression

Use `Required Validations`, not vague or optional `Suggested Validations`.

### 7. Questions

Group questions as:

- Critical
- Important
- Optional

Ask only questions that resolve a real business, security, testing, compatibility, or release ambiguity. Do not ask for facts already present in inspected evidence.

### 8. Proposed Test Coverage

Propose logical test groups by feature area, workflow stage, risk, platform, integration, deployment stage, or regression scope.

Explain the purpose of each group. Do not write detailed cases unless requested.

### 9. Evidence Reviewed / Could Not Verify / QA Assumptions

Report the evidence actually inspected, inaccessible material, and assumptions used.

'''

EXAMPLE_CONTENT = r'''# SMAR-2650 — Approved Requirement-Review Pattern

This file teaches the expected depth and structure for an INS LifeGuardian API/security ticket review. It is an analysis pattern, not a replacement for inspecting the current ticket and implementation.

## Evidence Pattern

A strong review should inspect more than the Jira summary. For SMAR-2650, the useful evidence types were:

- Current Jira description and expected behaviour
- Ticket history clarifying the exact affected methods and routes
- Parent HMAC security-remediation epic
- Existing ActivityMonitoringCriteria API documentation
- HMAC authentication usage documentation identifying endpoint consumers
- Relevant `serverless.yml`, function handlers, packaging output, and deployed API Gateway resources when available

## Weak vs Approved Reasoning

### Weak

`Risk: The API might not work correctly after merging the functions.`

### Approved

`Deployment Risk — High: Consolidating duplicate Serverless declarations may remove the /file/{Uuid} event, generate duplicate API Gateway methods, leave one method without Lambda invocation permission, or reference an unresolved authorizer import. Validate the source YAML, packaged CloudFormation, deployment events, deployed API Gateway methods, Lambda integration, and invocation permissions before runtime regression.`

### Weak

`Test invalid authentication.`

### Approved

`Verify both supported GET routes reject an API key without HMAC authentication, reject tampered or wrong-route signatures, and do not invoke the business Lambda or return criteria data. Confirm rejected requests are traceable without exposing API keys, HMAC secrets, valid signatures, or stack traces.`

## Required Review Shape

1. Requirement Summary
2. Scope
3. Missing Requirements and Gaps
4. Risk Analysis
5. Backend and Integration Impact
6. Required Validations
7. Questions
8. Proposed Test Coverage
9. Evidence Reviewed / Could Not Verify / QA Assumptions

## Quality Standard

A strong review:

- distinguishes configuration cleanup from functional implementation;
- identifies what must remain unchanged;
- finds conflicts between the ticket and older documentation;
- identifies active-consumer and backward-compatibility risk;
- analyses API Gateway, Lambda, authorizer, CloudFormation, data, and logs;
- states exact observable validation rather than `works correctly`;
- labels assumptions and unavailable evidence;
- does not generate detailed test cases before approval of the analysis and groups.
'''

PROMPT_TEMPLATE = r'''# INS LifeGuardian Requirement Review Prompt

Use this prompt when asking Codex to review a ticket deeply.

```text
Review ticket <TICKET-ID> in Requirement Review Mode.

Do not modify files and do not write detailed test cases in this response.

Use the Evidence Acquisition Gate in the INS LifeGuardian QA analyst skill.

Inspect all available evidence, including:
- Full Jira description and acceptance criteria
- Comments, relevant history, screenshots, and attachments
- Parent epic and directly related tickets
- Linked Confluence/API documentation
- Relevant source code, configuration, handlers, contracts, and tests
- Generated infrastructure or deployment output when applicable
- Relevant QA Second Brain knowledge

Return:
1. Requirement Summary
2. Scope
3. Missing Requirements and Gaps: Critical, Important, Optional
4. Risk Analysis
5. Backend and Integration Impact
6. Required Validations
7. Questions: Critical, Important, Optional
8. Proposed Test Coverage groups only
9. Evidence Reviewed, Could Not Verify, and QA Assumptions

Reference exact endpoint paths, HTTP methods, function names, handlers, YAML keys, fields, errors, files, and related tickets where evidence exists.

Do not infer that an endpoint is unused merely because its handler is missing.
Do not claim root cause or active consumer behaviour without evidence.
Identify conflicts between Jira, documentation, implementation, and stored QA knowledge.
Before finalizing, self-review for safety, security, data integrity, compatibility, deployment, integrations, logs, and cross-platform regression.
```
'''


def backup(path: Path, stamp: str) -> Path:
    backup_path = path.with_name(f"{path.name}.bak-{stamp}")
    shutil.copy2(path, backup_path)
    return backup_path


def insert_before(text: str, marker: str, content: str) -> str:
    if content.strip().splitlines()[0] in text:
        return text
    if marker not in text:
        raise ValueError(f"Insertion marker not found: {marker}")
    return text.replace(marker, content + marker, 1)


def replace_section(text: str, start_heading: str, next_heading: str, replacement: str) -> str:
    start = text.find(start_heading)
    if start < 0:
        raise ValueError(f"Section heading not found: {start_heading}")
    end = text.find(next_heading, start + len(start_heading))
    if end < 0:
        raise ValueError(f"Next section heading not found: {next_heading}")
    return text[:start] + replacement + text[end:]


def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repository", nargs="?", default=".")
    args = parser.parse_args()

    root = Path(args.repository).expanduser().resolve()
    agents = root / "AGENTS.md"
    skill = root / ".agents/skills/ins-lifeguardian-qa-analyst/SKILL.md"

    for required in (agents, skill):
        if not required.is_file():
            raise SystemExit(f"ERROR: Required file not found: {required}")

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backups: list[Path] = []

    agents_text = agents.read_text(encoding="utf-8")
    updated_agents = insert_before(agents_text, "## Skill Routing\n", AGENTS_EVIDENCE_SECTION)
    if updated_agents != agents_text:
        backups.append(backup(agents, stamp))
        agents.write_text(updated_agents, encoding="utf-8")
        print(f"UPDATED: {agents}")
    else:
        print(f"SKIPPED: Evidence-first section already exists in {agents}")

    skill_text = skill.read_text(encoding="utf-8")
    updated_skill = insert_before(
        skill_text,
        "## Automatic QA Second Brain Intake Rule\n",
        SKILL_EVIDENCE_SECTIONS,
    )
    updated_skill = replace_section(
        updated_skill,
        "## Default Requirement Intake Rule\n",
        "## Clarification Handling and Group Writing Rule\n",
        DEFAULT_INTAKE,
    )
    updated_skill = replace_section(
        updated_skill,
        "## Requirement Review Mode\n",
        "## API Analysis Mode\n",
        REQUIREMENT_REVIEW_MODE,
    )

    if updated_skill != skill_text:
        backups.append(backup(skill, stamp))
        skill.write_text(updated_skill, encoding="utf-8")
        print(f"UPDATED: {skill}")
    else:
        print(f"SKIPPED: Analyst skill already contains requested changes")

    example = (
        root
        / ".agents/skills/ins-lifeguardian-qa-analyst/references/examples/SMAR-2650-approved-review-pattern.md"
    )
    prompt = root / "qa-knowledge/templates/requirement-review-prompt.md"

    if write_if_missing(example, EXAMPLE_CONTENT):
        print(f"CREATED: {example}")
    else:
        print(f"SKIPPED: File already exists: {example}")

    if write_if_missing(prompt, PROMPT_TEMPLATE):
        print(f"CREATED: {prompt}")
    else:
        print(f"SKIPPED: File already exists: {prompt}")

    print("\nBackups created:")
    if backups:
        for item in backups:
            print(f"- {item}")
    else:
        print("- None (no existing file changed)")

    print("\nNext commands:")
    print("1. git diff -- AGENTS.md .agents/skills/ins-lifeguardian-qa-analyst/SKILL.md")
    print("2. git status")
    print("3. Test Codex with qa-knowledge/templates/requirement-review-prompt.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
