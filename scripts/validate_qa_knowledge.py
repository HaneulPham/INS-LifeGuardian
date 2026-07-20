#!/usr/bin/env python3
"""Validate INS LifeGuardian QA Second Brain structure and completion gates."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from validate_qa_test_cases import is_separator_row, is_table_row, normalize_header, split_markdown_row, table_rows, test_case_ids


KNOWLEDGE_STATUS_COLUMNS = ("Knowledge Item", "Source Status", "Source / Evidence", "Last Updated", "Notes")
ALLOWED_SOURCE_STATUSES = {"confirmed", "qa assumption", "open question", "out of scope", "deprecated", "conflict"}
MIGRATION_PLACEHOLDER_PATTERN = re.compile(
    r"\b(?:pending migration|migration pending)\b|\bhas not yet been (?:fully )?(?:migrated|copied)\b|\bhave not yet been (?:fully )?(?:migrated|copied)\b",
    re.I,
)


@dataclass(frozen=True)
class Issue:
    file: Path
    row: int
    item: str
    message: str


def find_table(lines: list[str], required_headers: tuple[str, ...]) -> tuple[int, list[str], list[tuple[int, list[str]]]] | None:
    required = {normalize_header(header) for header in required_headers}
    for index in range(len(lines) - 1):
        if not is_table_row(lines[index]) or not is_separator_row(lines[index + 1]):
            continue
        headers = split_markdown_row(lines[index])
        if required.issubset({normalize_header(header) for header in headers}):
            return index + 1, headers, table_rows(lines, index)
    return None


def section_content(text: str, heading: str) -> str | None:
    match = re.search(rf"^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s+|\Z)", text, re.M | re.S)
    return None if match is None else match.group(1).strip()


def section_applies(content: str) -> bool:
    normalized = re.sub(r"^[\s*-]+|[\s.]+$", "", content).casefold()
    return normalized not in {"", "none", "n/a", "not applicable"}


def validate_knowledge_status_files(project_root: Path) -> list[Issue]:
    issues: list[Issue] = []
    paths = sorted((project_root / "qa-knowledge/requirements").rglob("*.md"))
    paths.extend(sorted((project_root / "qa-knowledge/product/modules").rglob("*.md")))
    expected = [normalize_header(column) for column in KNOWLEDGE_STATUS_COLUMNS]
    for path in paths:
        lines = path.read_text(encoding="utf-8").splitlines()
        shown = path.relative_to(project_root)
        heading = next((i for i, line in enumerate(lines) if normalize_header(line.lstrip("# ")) == "knowledge status"), None)
        if heading is None:
            issues.append(Issue(shown, 0, "<none>", "missing Knowledge Status section"))
            continue
        table = find_table(lines[heading + 1 :], ("Knowledge Item",))
        if table is None:
            issues.append(Issue(shown, heading + 1, "<none>", "missing Knowledge Status table"))
            continue
        table_row, headers, rows = table
        if [normalize_header(header) for header in headers] != expected:
            issues.append(Issue(shown, heading + table_row + 1, "<table>", "Knowledge Status columns must be: " + ", ".join(KNOWLEDGE_STATUS_COLUMNS)))
            continue
        if not rows:
            issues.append(Issue(shown, heading + table_row + 1, "<table>", "Knowledge Status table has no knowledge rows"))
            continue
        header_map = {normalize_header(header): position for position, header in enumerate(headers)}
        for row_number, cells in rows:
            def value(column: str) -> str:
                position = header_map[normalize_header(column)]
                return cells[position].strip() if position < len(cells) else ""
            status = normalize_header(value("Source Status"))
            if status not in ALLOWED_SOURCE_STATUSES:
                issues.append(Issue(shown, heading + row_number + 1, "<knowledge>", f"unsupported Source Status {value('Source Status')!r}"))
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value("Last Updated")) is None:
                issues.append(Issue(shown, heading + row_number + 1, "<knowledge>", "Last Updated must use YYYY-MM-DD"))
    return issues


def validate_ticket_index(project_root: Path) -> list[Issue]:
    issues: list[Issue] = []
    index_path = project_root / "qa-knowledge/ticket-index.md"
    shown_index = index_path.relative_to(project_root)
    if not index_path.is_file():
        return [Issue(shown_index, 0, "<none>", "ticket index does not exist")]
    table = find_table(index_path.read_text(encoding="utf-8").splitlines(), ("Ticket", "Requirement File", "Test Case File", "Status"))
    if table is None:
        return [Issue(shown_index, 0, "<none>", "ticket index table is missing")]
    _, headers, rows = table
    header_map = {normalize_header(header): position for position, header in enumerate(headers)}
    decision_path = project_root / "qa-knowledge/decisions/decision-log.md"
    regression_path = project_root / "qa-knowledge/regression/regression-map.md"
    decision_text = decision_path.read_text(encoding="utf-8") if decision_path.is_file() else ""
    regression_text = regression_path.read_text(encoding="utf-8") if regression_path.is_file() else ""
    for row_number, cells in rows:
        def value(column: str) -> str:
            position = header_map[normalize_header(column)]
            return cells[position].strip() if position < len(cells) else ""
        ticket = value("Ticket") or "<missing>"
        requirement = project_root / "qa-knowledge" / value("Requirement File")
        test_cases = project_root / "qa-knowledge" / value("Test Case File")
        for label, path in (("requirement", requirement), ("test-case", test_cases)):
            if not path.is_file():
                issues.append(Issue(shown_index, row_number, ticket, f"indexed {label} file does not exist: {path.relative_to(project_root)}"))
        if value("Status").casefold() != "completed" or not requirement.is_file() or not test_cases.is_file():
            continue
        requirement_text = requirement.read_text(encoding="utf-8")
        test_text = test_cases.read_text(encoding="utf-8")
        for label, path, content in (("requirement", requirement, requirement_text), ("test-case", test_cases, test_text)):
            if MIGRATION_PLACEHOLDER_PATTERN.search(content):
                issues.append(Issue(path.relative_to(project_root), 0, ticket, f"Completed ticket still contains a {label} migration placeholder"))
        ids = test_case_ids(test_cases)
        if not ids:
            issues.append(Issue(test_cases.relative_to(project_root), 0, ticket, "Completed ticket has no approved test-case rows"))
        elif not any(tc_id.startswith(f"{ticket}-") for tc_id in ids):
            issues.append(Issue(test_cases.relative_to(project_root), 0, ticket, "Completed ticket has no test-case rows using its ticket ID"))
        if not re.search(r"^##\s+Group\s+\d+\b", test_text, re.M):
            issues.append(Issue(test_cases.relative_to(project_root), 0, ticket, "Completed ticket has no stored approved test-case group"))
        for section, log_text, log_name in (("Confirmed Decisions", decision_text, "decision log"), ("Regression Risk", regression_text, "regression map")):
            content = section_content(requirement_text, section)
            if content is None:
                issues.append(Issue(requirement.relative_to(project_root), 0, ticket, f"Completed requirement is missing ## {section}; use None when not applicable"))
            elif section_applies(content) and ticket not in log_text:
                issues.append(Issue(requirement.relative_to(project_root), 0, ticket, f"{section} applies but {ticket} is absent from the {log_name}"))
    return issues


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate QA Second Brain knowledge.")
    parser.add_argument("path", nargs="?", type=Path, default=Path(__file__).resolve().parent.parent)
    return parser.parse_args()


def main() -> int:
    root = parse_args().path.resolve()
    issues = validate_knowledge_status_files(root) + validate_ticket_index(root)
    if not issues:
        print("PASS")
        return 0
    for issue in issues:
        print(f"FAIL file={issue.file} row={issue.row} item={issue.item} issue={issue.message}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
