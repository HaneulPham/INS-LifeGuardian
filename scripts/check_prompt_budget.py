#!/usr/bin/env python3
"""Guard INS LifeGuardian Codex prompt surfaces against token creep.

The limits are character budgets, not model-token guarantees. They keep always-on
instructions compact and preserve progressive disclosure for task references.
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

FILES = {
    "AGENTS": ROOT / "AGENTS.md",
    "ANALYST_SKILL": ROOT / ".agents/skills/ins-lifeguardian-qa-analyst/SKILL.md",
    "INTAKE": ROOT / ".agents/skills/ins-lifeguardian-qa-analyst/references/requirement-intake.md",
    "CASE_STYLE": ROOT / ".agents/skills/ins-lifeguardian-qa-analyst/references/test-case-style.md",
    "CASE_GATE": ROOT / ".agents/skills/ins-lifeguardian-qa-analyst/references/test-case-quality-gate.md",
    "COMMANDS": ROOT / ".agents/skills/ins-lifeguardian-qa-analyst/references/workflow-commands.md",
    "API_AUTOMATION": ROOT / ".agents/skills/ins-lifeguardian-playwright-api-automation/SKILL.md",
}

LIMITS = {
    "AGENTS": 7_600,
    "ANALYST_SKILL": 7_800,
    "INTAKE": 4_200,
    "CASE_STYLE": 6_500,
    "COMMANDS": 4_500,
    "API_AUTOMATION": 6_500,
}

FLOW_LIMITS = {
    "default_intake": ("AGENTS", "ANALYST_SKILL", "INTAKE", 19_500),
    "detailed_cases": ("AGENTS", "ANALYST_SKILL", "CASE_STYLE", "CASE_GATE", 25_000),
    "command_routing": ("AGENTS", "ANALYST_SKILL", "COMMANDS", 19_000),
    "api_automation": ("AGENTS", "API_AUTOMATION", 14_500),
}

FORBIDDEN = {
    "AGENTS": (
        "For every INS LifeGuardian QA task, read relevant knowledge in this order",
        "Every completed review must include",
    ),
    "ANALYST_SKILL": (
        "Read `references/project-scope.md` for every task",
        "read the full test-case style, quality gate, and approved SMAR-2633 pattern",
    ),
}


def estimate_tokens(characters: int) -> int:
    return round(characters / 4)


def main() -> int:
    failures: list[str] = []
    sizes: dict[str, int] = {}
    texts: dict[str, str] = {}

    for name, path in FILES.items():
        if not path.is_file():
            failures.append(f"missing file: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        texts[name] = text
        sizes[name] = len(text)

    for name, limit in LIMITS.items():
        actual = sizes.get(name, 0)
        if actual > limit:
            failures.append(f"{name}: {actual:,} chars exceeds {limit:,}")

    for flow, spec in FLOW_LIMITS.items():
        *names, limit = spec
        actual = sum(sizes.get(name, 0) for name in names)
        if actual > limit:
            failures.append(f"{flow}: {actual:,} chars exceeds {limit:,}")

    for name, phrases in FORBIDDEN.items():
        text = texts.get(name, "")
        for phrase in phrases:
            if phrase in text:
                failures.append(f"{name}: broad mandatory-load phrase returned: {phrase!r}")

    print("INS LifeGuardian prompt budget")
    for name, size in sizes.items():
        print(f"- {name}: {size:,} chars (~{estimate_tokens(size):,} tokens)")
    for flow, spec in FLOW_LIMITS.items():
        *names, _ = spec
        size = sum(sizes.get(name, 0) for name in names)
        print(f"- {flow}: {size:,} chars (~{estimate_tokens(size):,} tokens before task evidence)")

    if failures:
        print("\nFAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("\nPASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
