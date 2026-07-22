# INS LifeGuardian Requirement Review Prompt

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
7. Questions: Critical, Important, Optional, using one decision per question with concrete selectable behaviours
8. Proposed Test Coverage groups only
9. Evidence Reviewed, Could Not Verify, and QA Assumptions

Reference exact endpoint paths, HTTP methods, function names, handlers, YAML keys, fields, errors, files, and related tickets where evidence exists.

Do not infer that an endpoint is unused merely because its handler is missing.
Do not claim root cause or active consumer behaviour without evidence.
Identify conflicts between Jira, documentation, implementation, and stored QA knowledge.
Before finalizing, self-review for safety, security, privacy, data integrity, test-data isolation/cleanup, required instrumentation, compatibility, deployment, integrations, logs, and cross-platform regression.
```
