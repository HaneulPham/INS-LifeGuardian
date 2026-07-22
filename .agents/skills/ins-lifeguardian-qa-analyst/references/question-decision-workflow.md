# Questions and confirmed-decision workflow

Use this reference whenever missing or conflicting behaviour requires a product, BA, developer, permission, safety, data, integration, or operational decision.

## Ask the smallest useful set

- Ask only questions that materially change implementation, expected results, priority, data setup, integration behaviour, or regression scope.
- Ask one decision per question.
- Do not repeat information already answered by Jira, comments, screenshots, API documentation, verified behaviour, the active conversation, or Confirmed Second Brain knowledge.
- Present Critical questions first. Limit the initial decision set to the highest-leverage items; defer low-risk Optional questions until they become relevant.
- A reviewer observation may prove a coverage gap without defining the expected business behaviour. Do not convert it into a confirmed rule.

## Selectable format

```markdown
Q1. <One clear decision question>

Why this matters:
- <Business, safety, data, permission, integration, operational, or test impact>

Options:
- A. <Concrete product behaviour>
- B. <Concrete product behaviour>
- C. <Concrete product behaviour>
- D. Other – specify

QA Recommendation: Option A
```

Rules:

- Provide two to five concrete behaviour options when practical, plus `Other – specify` when the valid choices may be broader.
- Avoid bare Yes/No options when the resulting behaviour can be stated directly.
- Add a QA recommendation only when evidence, safety, consistency, or fail-safe design supports it. Omit the recommendation when the choice is a business or permission decision with no safe default.
- Allow compact answers such as `Q1-A, Q2-C`.

## After an answer

For every selected answer:

1. Record it under **Confirmed Decisions**, including its source and date when known.
2. Close the question; do not keep it under Open Questions.
3. Update requirement summary, scope, risks, assumptions, validations, coverage groups, and affected cases.
4. Identify test cases to **Add**, **Update**, **Merge**, **Remove**, or **Defer**.
5. Preserve unaffected approved cases and IDs.
6. Re-run duplicate review when the decision changes coverage.

For an unanswered non-blocking question, continue with a clearly labelled **QA Assumption**. For an unanswered Critical question, provide best-effort analysis and preliminary coverage, identify the cases that require revision, and do not invent an executable expected result.
