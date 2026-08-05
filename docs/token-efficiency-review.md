# INS LifeGuardian Codex Token-Efficiency Review

Date: 2026-08-05

## Problem found

The previous architecture had good QA safeguards but loaded too much context by default:

- `AGENTS.md` and the Analyst skill repeated evidence, intake, Second Brain, case, and feedback rules.
- Every QA task was instructed to read the broad QA Second Brain sequence, including regression and decision logs even when unrelated.
- Detailed case requests always loaded project scope, style, quality gate, and the full approved example.
- Automatic intake required a long seven-part response plus generic next prompts.
- No automated check prevented prompt files from growing again.

## Changes made

- Added a minimum-context rule and task-targeted Second Brain retrieval.
- Replaced broad mandatory reference loading with selective reference routing.
- Made default intake concise; `analytics` now explicitly requests deep analysis.
- Made approved examples conditional rather than mandatory for every detailed group.
- Kept detailed-case quality, traceability, privacy, instrumentation, cleanup, ID, and review gates.
- Added platform-neutral regression output.
- Added `scripts/check_prompt_budget.py`, CI execution, unit checks, and token-efficiency behaviour evals.

## Estimated instruction overhead

Character counts are converted at approximately four characters per token. Actual model tokenization varies.

| Flow | Previous | Updated | Estimated reduction |
|---|---:|---:|---:|
| Always-on AGENTS + Analyst skill | 18,884 chars (~4,721 tokens) | 14,461 chars (~3,615 tokens) | 23% |
| Default requirement intake | 27,613 chars (~6,903 tokens) | 18,273 chars (~4,568 tokens) | 34% |
| Detailed case generation | 39,066 chars (~9,766 tokens) | 24,017 chars (~6,004 tokens) | 39% |

The table excludes the larger contextual saving from removing the mandatory full QA Second Brain scan.

## Validation

- 61 unit tests pass.
- QA knowledge validation passes.
- QA test-case validation passes.
- Prompt-budget validation passes.

## Remaining concerns

1. Behaviour can be made consistent, but Codex and ChatGPT cannot be guaranteed to produce identical wording or reasoning on every run.
2. Actual context use depends on Codex following selective routing; manual behaviour evals should continue after major instruction changes.
3. `regression-map.md` and `decision-log.md` remain large. Targeted search avoids routine loading, but splitting them by module or ticket family would improve retrieval as they grow.
4. Test-case priority is standardized to `High`, `Medium`, or `Low`; the validator rejects any other value.
5. Complete-suite requests remain expensive by nature; the user’s explicit batch request should continue to override group-by-group review.
6. Jira/Confluence evidence quality depends on MCP availability and approval. Missing private evidence must remain `Could Not Verify`.
7. The original archive included `.git`, `.cache`, `.backups`, and macOS metadata. Distribution archives should exclude them.
