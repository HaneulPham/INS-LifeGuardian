# INS LifeGuardian Codex — Final Improvement Summary

## Final command workflow

- `analytics` — any evidence-backed ticket QA analysis except detailed test-case rows and file writes.
- `write test cases [for G#|all]` — write requested approved groups only.
- `review test cases` — apply the complete quality gate without changing unrelated cases.
- `Update test cases to Second Brain` — direct Confluence-to-Second-Brain execution: retrieve, review, safely normalize, update, validate, and report; no second approval phrase.
- `write a bug` — one Jira-ready evidence-backed defect.
- `write API automation` — implement approved API cases using the existing framework and contracts.

## Quality and safety

- Only High, Medium, and Low test-case priorities are accepted.
- Requirements, decisions, assumptions, risks, gaps, groups, and cases remain distinctly traceable.
- Detailed cases require observable outcomes, evidence-backed integration expectations, privacy-safe data, and safe cleanup.
- Confluence updates preserve unique coverage and history; unsupported behaviour is never invented.
- Evidence-backed Conflict/GAP records may be stored while unrelated valid content is updated; conflicted tickets remain incomplete.
- Direct updates use clean-worktree, backup, sensitive-content, target/create, and strict validation gates with rollback on failure.

## Token efficiency

The project uses progressive disclosure. Always-on instructions remain compact; task references, examples, stored knowledge, and API automation instructions load only when relevant. The command-routing prompt remains under its configured budget.

## Validation

Run:

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
python3 scripts/validate_qa_test_cases.py
python3 scripts/validate_qa_knowledge.py
python3 scripts/check_prompt_budget.py
```
