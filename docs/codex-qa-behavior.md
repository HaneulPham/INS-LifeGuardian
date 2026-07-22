# Codex QA Behaviour Architecture

This repository uses three layers to make Codex behave consistently as an INS LifeGuardian Senior QA Analyst.

## 1. `AGENTS.md` — always-on project rules

Codex reads repository `AGENTS.md` before work begins. It contains the project-wide evidence gate, workflow routing, default one-group-at-a-time rule with explicit complete-suite override, title/ID conventions, question/decision handling, feedback handling, instrumentation/privacy/cleanup requirements, and Second Brain safety gates.

Keep `AGENTS.md` compact and use it for rules that must apply to every QA task.

## 2. QA Analyst skill — task-specific expertise

`.agents/skills/ins-lifeguardian-qa-analyst/` contains:

- `SKILL.md` for routing and the high-level workflow;
- reference files for intake, review, API, regression, bugs, detailed cases, feedback, and the quality gate;
- approved examples that demonstrate the expected depth and format.

The SMAR-2633 approved pattern is the primary detailed-case example. Update it when the user approves a materially better pattern.

## 3. Validators and evals — drift protection

- `scripts/validate_qa_test_cases.py` checks IDs, priorities, group matching, title style, navigation, numbered steps, step references, API methods/statuses, vague wording, and duplicates.
- `scripts/validate_qa_knowledge.py` protects Second Brain structure and status integrity.
- `tests/` prevents validator and instruction regressions.
- `qa-evals/codex-behavior-evals.md` provides manual model-behaviour scenarios that static validation cannot fully prove.

## Recommended workflow

1. Start Codex from the repository root so root `AGENTS.md` and `.agents/skills` are discovered.
2. Provide the Jira ticket, link, screenshots, comments, or attachments.
3. Let Automatic Requirement Intake produce analysis and groups.
4. Use `Write detailed test cases for Group 1 only.`
5. Review and correct the group.
6. Use `next` for each approved group.
7. Give Rovo/BA/Dev feedback; Codex first classifies Add/Update/Merge/Remove/Defer/Reject.
8. When all content is approved, use the exact Second Brain approval command.
9. Run validators and unit tests before committing.

## Validation commands

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
python3 scripts/validate_qa_test_cases.py
python3 scripts/validate_qa_knowledge.py
```

## Important limitation

Instructions and examples strongly improve consistency, but they do not guarantee identical wording on every run. The validators catch structural drift, while the behaviour evals are used to compare reasoning and workflow decisions that cannot be enforced by Markdown parsing alone.
