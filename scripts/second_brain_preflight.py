#!/usr/bin/env python3
"""Machine-enforce configured safety gates before Second Brain writes."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


TICKET_PATTERN = re.compile(r"^(?:SMAR|MA)-\d+$")
MIGRATION_PATTERN = re.compile(
    r"\b(?:pending migration|migration pending)\b|\bhas not yet been (?:fully )?(?:migrated|copied)\b|\bhave not yet been (?:fully )?(?:migrated|copied)\b",
    re.I,
)
CONFLICT_ROW_PATTERN = re.compile(r"\|\s*Conflict\s*\|", re.I)
SENSITIVE_PATTERNS = (
    ("credential or secret", re.compile(r"(?i)\b(?:api[_ -]?key|access[_ -]?token|password|secret)\s*[:=]\s*\S+")),
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("possible phone number", re.compile(r"(?i)\b(?:phone|mobile|telephone)\s*:\s*\+?\d[\d ()-]{7,}\d")),
    ("possible client or patient identity", re.compile(r"(?i)\b(?:client|patient)\s+(?:name|address|date of birth|dob)\s*:\s*\S+")),
)
BOOLEAN_KEYS = {
    "auto_apply_second_brain_updates",
    "require_exact_approval_phrase",
    "require_clean_worktree",
    "create_backup",
    "run_test_case_validation",
    "run_knowledge_validation",
    "stop_on_conflict",
    "stop_on_open_migration",
    "block_sensitive_data",
    "update_ticket_index",
    "update_regression_map",
    "update_decision_log",
}


def parse_scalar(value: str) -> object:
    value = value.strip()
    if value.casefold() == "true":
        return True
    if value.casefold() == "false":
        return False
    return value.strip("'\"")


def load_automation_config(path: Path) -> tuple[dict[str, object], list[str]]:
    """Parse the repository's intentionally flat automation YAML section."""
    settings: dict[str, object] = {}
    issues: list[str] = []
    in_automation = False
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = raw_line.split("#", 1)[0].rstrip()
        if not stripped:
            continue
        if not raw_line.startswith((" ", "\t")):
            in_automation = stripped == "automation:"
            continue
        if not in_automation:
            continue
        match = re.fullmatch(r"\s+([a-z0-9_]+):\s*(.*?)\s*", stripped)
        if match is None:
            issues.append(f"config line {line_number} is not a supported key/value")
            continue
        settings[match.group(1)] = parse_scalar(match.group(2))
    missing = sorted(BOOLEAN_KEYS - settings.keys())
    if missing:
        issues.append("missing automation setting(s): " + ", ".join(missing))
    for key in sorted(BOOLEAN_KEYS & settings.keys()):
        if not isinstance(settings[key], bool):
            issues.append(f"automation.{key} must be true or false")
    if not isinstance(settings.get("backup_directory"), str) or not settings.get("backup_directory"):
        issues.append("automation.backup_directory must be a non-empty path")
    return settings, issues


def run_git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(("git", *args), cwd=root, text=True, capture_output=True, check=False)


def ticket_paths(root: Path, ticket: str) -> tuple[Path, Path]:
    project = ticket.split("-", 1)[0]
    return (
        root / "qa-knowledge/requirements" / project / f"{ticket}.md",
        root / "qa-knowledge/test-cases" / project / f"{ticket}.md",
    )


def inspect_sensitive_text(paths: list[Path]) -> list[str]:
    issues: list[str] = []
    for path in paths:
        if not path.is_file():
            issues.append(f"proposed content file does not exist: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        for label, pattern in SENSITIVE_PATTERNS:
            if pattern.search(text):
                issues.append(f"{path}: {label} detected")
    return issues


def evaluate(
    root: Path,
    approval_phrase: str,
    ticket: str,
    proposed_files: list[Path],
    migration: bool,
) -> list[str]:
    config_path = root / "qa-knowledge/config.yml"
    if not config_path.is_file():
        return ["qa-knowledge/config.yml does not exist"]
    settings, issues = load_automation_config(config_path)
    if issues:
        return issues
    if not settings.get("auto_apply_second_brain_updates"):
        issues.append("automatic Second Brain updates are disabled")
    if not TICKET_PATTERN.fullmatch(ticket):
        issues.append("ticket must match SMAR-<number> or MA-<number>")
        return issues
    expected_phrase = f"Approve and Update the QA Second Brain for ticket {ticket}"
    if settings.get("require_exact_approval_phrase") and approval_phrase != expected_phrase:
        issues.append("exact approval phrase is missing or does not match the ticket")

    requirement, test_cases = ticket_paths(root, ticket)
    for path in (requirement, test_cases):
        if not path.is_file():
            issues.append(f"target file does not exist: {path.relative_to(root)}")

    if settings.get("require_clean_worktree"):
        status = run_git(root, "status", "--porcelain")
        if status.returncode != 0:
            issues.append("could not inspect Git worktree")
        elif status.stdout.strip():
            paths = [line[3:] for line in status.stdout.splitlines()]
            issues.append("worktree is not clean: " + ", ".join(paths))

    existing_paths = [path for path in (requirement, test_cases) if path.is_file()]
    if settings.get("stop_on_open_migration") and not migration:
        for path in existing_paths:
            if MIGRATION_PATTERN.search(path.read_text(encoding="utf-8")):
                issues.append(f"open migration placeholder: {path.relative_to(root)}")
    if settings.get("stop_on_conflict"):
        for path in existing_paths:
            if CONFLICT_ROW_PATTERN.search(path.read_text(encoding="utf-8")):
                issues.append(f"unresolved Conflict status: {path.relative_to(root)}")

    if settings.get("block_sensitive_data"):
        if not proposed_files:
            issues.append("no proposed content file supplied for sensitive-data inspection")
        else:
            resolved_proposals = [path if path.is_absolute() else root / path for path in proposed_files]
            issues.extend(inspect_sensitive_text(resolved_proposals))

    if settings.get("create_backup"):
        backup_directory = root / str(settings["backup_directory"])
        probe = backup_directory / ".preflight-probe"
        ignored = run_git(root, "check-ignore", "--quiet", str(probe))
        if ignored.returncode != 0:
            issues.append(f"backup directory is not ignored by Git: {backup_directory.relative_to(root)}")
    return issues


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check safety gates before a Second Brain update.")
    parser.add_argument("--approval-phrase", required=True)
    parser.add_argument("--ticket", required=True)
    parser.add_argument("--proposed-file", action="append", type=Path, default=[])
    parser.add_argument("--migration", action="store_true", help="allow known placeholders only for an explicit, evidence-backed migration")
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parent.parent)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    issues = evaluate(args.project_root.resolve(), args.approval_phrase, args.ticket, args.proposed_file, args.migration)
    if not issues:
        print(f"PASS ticket={args.ticket}")
        return 0
    for issue in issues:
        print(f"FAIL ticket={args.ticket} issue={issue}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
