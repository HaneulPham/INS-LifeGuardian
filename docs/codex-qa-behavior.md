# Codex QA Behaviour Architecture

The repository uses progressive disclosure so Codex can preserve INS LifeGuardian QA depth without loading every instruction and knowledge file for every request.

## 1. `AGENTS.md` — compact always-on contract

`AGENTS.md` contains only project-wide gates: role, evidence priority, minimum-context retrieval, response selection, question/traceability rules, detailed-case essentials, privacy, and stored-knowledge safety.

It must not require a full QA Second Brain scan or every reference/example on every task.

## 2. Analyst skill — selective task router

`.agents/skills/ins-lifeguardian-qa-analyst/SKILL.md` maps each request to the smallest relevant reference set.

Examples:

- concise evidence intake → `requirement-intake.md`;
- formal review → `requirement-review.md`;
- detailed cases → `test-case-style.md` plus `test-case-quality-gate.md`;
- API, regression, bug, feedback, or questions → only the corresponding reference;
- approved examples → only for explicit comparison, drift review, or format uncertainty.

The skill also defines targeted QA Second Brain retrieval. A known ticket opens its exact index links; module, regression, decision, and status files are loaded only when the task needs them.

## 3. Response depth

Default intake is intentionally lean:

1. Requirement Summary
2. Material QA Findings
3. Blocking or material Questions
4. Proposed Test Groups
5. Material evidence limitations/assumptions, when present

`analytics` requests the deep review. Detailed cases remain group-by-group by default, with an explicit complete-suite override.


## Canonical command workflow

The project recognizes `analytics`, `write test cases`, `review test cases`, `Update test cases to Second Brain`, `write a bug`, and `write API automation` as explicit workflow intents. Their strict boundaries live in `references/workflow-commands.md`; API implementation is isolated in the progressive-disclosure `ins-lifeguardian-api-automation` skill.

Completion output may include one context-specific `Suggested next command:` line. Generic menus are prohibited, and Second Brain storage is not suggested until the requested cases pass review.

## 4. Drift protection

- `scripts/check_prompt_budget.py` limits prompt-surface growth and detects broad mandatory-load language.
- `scripts/validate_qa_test_cases.py` validates IDs, priorities, titles, steps, outcomes, and duplicates.
- `scripts/validate_qa_knowledge.py` protects Second Brain structure and status integrity.
- `tests/test_qa_behavior_contract.py` checks behavioural and token-efficiency contracts.
- `qa-evals/codex-behavior-evals.md` covers model behaviours that static checks cannot prove.

## Recommended workflow

1. Start Codex from the repository root.
2. Supply current evidence.
3. Use concise intake or a narrow command (`summary`, `questions`, `groups`, `api`, `regression`).
4. Use `analytics` only when deeper analysis is required.
5. Use `write test cases for G1`, then `review test cases`; use `next` only after approval.
6. Use `Update test cases to Second Brain` with supplied Confluence cases for direct Librarian review, normalization, storage, and validation.
7. Use `write a bug` or `write API automation` only for those artifacts.
8. Run validation before committing.

## Validation commands

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
python3 scripts/check_prompt_budget.py
python3 scripts/validate_qa_test_cases.py
python3 scripts/validate_qa_knowledge.py
```

## Limitation

Instruction routing improves consistency and reduces context cost, but cannot guarantee identical wording on every run. Static checks enforce structure and budgets; behaviour evals remain necessary for reasoning quality.
