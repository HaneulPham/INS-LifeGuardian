#!/usr/bin/env python3
"""Validate INS LifeGuardian UI, API, and regression test-case tables."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


UI_COLUMNS = (
    "TC ID", "Priority", "Test Area", "Title", "Preconditions", "Test Steps",
    "Expected Result", "Expected Integration", "Notes",
)
API_COLUMNS = (
    "TC ID", "Priority", "API Endpoint", "Method", "Title", "Preconditions",
    "Request Data", "Expected Response", "Notes",
)
REGRESSION_COLUMNS = (
    "ID", "Priority", "Test Area", "Summary", "Preconditions", "Test Steps",
    "Check on CP", "Check on Portal", "Integration Check",
)
SCHEMAS = {
    "UI/Mobile": UI_COLUMNS,
    "API": API_COLUMNS,
    "Regression": REGRESSION_COLUMNS,
}
ALLOWED_PRIORITIES = ("High", "Medium", "Low", "Lowest")
TC_ID_PATTERN = re.compile(r"^(?:SMAR|MA)-\d+-G\d+-\d{2}$")
NUMBERED_STEP_PATTERN = re.compile(r"(?:^|\n|<br\s*/?>)\s*1[.)]\s+\S", re.I)
STEP_NUMBER_PATTERN = re.compile(r"(?:^|\n|<br\s*/?>)\s*(\d+)[.)]\s+\S", re.I)
VERIFY_REFERENCE_PATTERN = re.compile(r"\*\*Verify after step\s+#?(\d+)\s*:?\*\*", re.I)


@dataclass(frozen=True)
class Issue:
    file: Path
    row: int
    tc_id: str
    message: str


def split_markdown_row(line: str) -> list[str]:
    """Split a Markdown table row while preserving escaped pipes."""
    text = line.strip()
    if text.startswith("|"):
        text = text[1:]
    if text.endswith("|") and not text.endswith(r"\|"):
        text = text[:-1]
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for character in text:
        if character == "|" and not escaped:
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(character)
        escaped = character == "\\" and not escaped
    cells.append("".join(current).strip())
    return [cell.replace(r"\|", "|") for cell in cells]


def is_separator_row(line: str) -> bool:
    cells = split_markdown_row(line)
    return bool(cells) and all(
        re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) is not None
        for cell in cells
    )


def normalize_header(value: str) -> str:
    return " ".join(value.replace("`", "").replace("**", "").split()).casefold()


def is_table_row(line: str) -> bool:
    return "|" in line and bool(line.strip())


def display_path(path: Path, scan_root: Path) -> Path:
    try:
        return path.relative_to(scan_root.parent.parent)
    except ValueError:
        return path


def detect_schema(headers: list[str]) -> str | None:
    normalized = {normalize_header(header) for header in headers}
    if {"api endpoint", "method"}.issubset(normalized):
        return "API"
    if {"check on cp", "integration check"}.issubset(normalized):
        return "Regression"
    if {"expected result", "expected integration"}.issubset(normalized):
        return "UI/Mobile"
    return None


def table_rows(lines: list[str], header_index: int) -> list[tuple[int, list[str]]]:
    rows: list[tuple[int, list[str]]] = []
    row_index = header_index + 2
    while row_index < len(lines) and is_table_row(lines[row_index]):
        if not is_separator_row(lines[row_index]):
            rows.append((row_index + 1, split_markdown_row(lines[row_index])))
        row_index += 1
    return rows


def test_case_ids(path: Path) -> list[str]:
    """Return IDs from all recognized test-case tables."""
    lines = path.read_text(encoding="utf-8").splitlines()
    ids: list[str] = []
    for index in range(len(lines) - 1):
        if not is_table_row(lines[index]) or not is_separator_row(lines[index + 1]):
            continue
        headers = split_markdown_row(lines[index])
        schema = detect_schema(headers)
        if schema is None:
            continue
        normalized = [normalize_header(header) for header in headers]
        id_column = "id" if schema == "Regression" else "tc id"
        if id_column not in normalized:
            continue
        position = normalized.index(id_column)
        for _, cells in table_rows(lines, index):
            if position < len(cells) and cells[position].strip():
                ids.append(cells[position].strip())
    return ids


def validate_step_references(
    shown_path: Path,
    row: int,
    tc_id: str,
    test_steps: str,
    expected_fields: list[tuple[str, str]],
) -> list[Issue]:
    issues: list[Issue] = []
    step_numbers = {int(value) for value in STEP_NUMBER_PATTERN.findall(test_steps)}
    for label, content in expected_fields:
        references = {int(value) for value in VERIFY_REFERENCE_PATTERN.findall(content)}
        if not references:
            issues.append(Issue(shown_path, row, tc_id, f"{label} must contain a '**Verify after step #N:**' marker"))
            continue
        missing = sorted(references - step_numbers)
        if missing:
            issues.append(Issue(shown_path, row, tc_id, f"{label} references missing step(s): {', '.join(map(str, missing))}"))
    return issues


def validate_file(
    path: Path,
    scan_root: Path,
    seen_ids: dict[str, tuple[Path, int]],
) -> tuple[list[Issue], int]:
    issues: list[Issue] = []
    rows_found = 0
    lines = path.read_text(encoding="utf-8").splitlines()
    index = 0
    while index + 1 < len(lines):
        if not is_table_row(lines[index]) or not is_separator_row(lines[index + 1]):
            index += 1
            continue
        headers = split_markdown_row(lines[index])
        schema = detect_schema(headers)
        if schema is None:
            index += 2
            continue
        normalized_headers = [normalize_header(header) for header in headers]
        header_map = {header: position for position, header in enumerate(normalized_headers)}
        required_columns = SCHEMAS[schema]
        missing = [column for column in required_columns if normalize_header(column) not in header_map]
        shown_path = display_path(path, scan_root)
        if missing:
            issues.append(Issue(shown_path, index + 1, "<table>", f"{schema} table missing required columns: {', '.join(missing)}"))

        row_index = index + 2
        while row_index < len(lines) and is_table_row(lines[row_index]):
            if is_separator_row(lines[row_index]):
                row_index += 1
                continue
            cells = split_markdown_row(lines[row_index])
            if not any(cell.strip() for cell in cells):
                row_index += 1
                continue
            rows_found += 1
            if len(cells) < len(headers):
                cells.extend([""] * (len(headers) - len(cells)))

            def value(column: str) -> str:
                position = header_map.get(normalize_header(column))
                return "" if position is None or position >= len(cells) else cells[position].strip()

            id_column = "ID" if schema == "Regression" else "TC ID"
            tc_id = value(id_column) or "<missing>"
            source_row = row_index + 1
            if tc_id == "<missing>" or not TC_ID_PATTERN.fullmatch(tc_id):
                issues.append(Issue(shown_path, source_row, tc_id, "invalid TC ID format"))
            else:
                file_ticket = path.stem if re.fullmatch(r"(?:SMAR|MA)-\d+", path.stem) else None
                if file_ticket and not tc_id.startswith(f"{file_ticket}-"):
                    issues.append(Issue(shown_path, source_row, tc_id, f"TC ID prefix must match file ticket {file_ticket}"))
                if tc_id in seen_ids:
                    first_file, first_row = seen_ids[tc_id]
                    issues.append(Issue(shown_path, source_row, tc_id, f"duplicate TC ID; first found in {first_file} row {first_row}"))
                else:
                    seen_ids[tc_id] = (shown_path, source_row)

            priority = value("Priority")
            if priority not in ALLOWED_PRIORITIES:
                issues.append(Issue(shown_path, source_row, tc_id, f"invalid Priority {priority!r}; allowed: {', '.join(ALLOWED_PRIORITIES)}"))

            for column in required_columns:
                if not value(column):
                    issues.append(Issue(shown_path, source_row, tc_id, f"{column} must not be empty"))

            if schema in {"UI/Mobile", "Regression"}:
                test_steps = value("Test Steps")
                if not NUMBERED_STEP_PATTERN.search(test_steps):
                    issues.append(Issue(shown_path, source_row, tc_id, "Test Steps must use numbered steps beginning with 1"))
                expected = (
                    [("Expected Result", value("Expected Result")), ("Expected Integration", value("Expected Integration"))]
                    if schema == "UI/Mobile"
                    else [("Check on CP", value("Check on CP")), ("Check on Portal", value("Check on Portal")), ("Integration Check", value("Integration Check"))]
                )
                issues.extend(validate_step_references(shown_path, source_row, tc_id, test_steps, expected))
            row_index += 1
        index = row_index
    return issues, rows_found


def parse_args() -> argparse.Namespace:
    default_root = Path(__file__).resolve().parent.parent / "qa-knowledge/test-cases"
    parser = argparse.ArgumentParser(description="Validate Markdown QA test cases.")
    parser.add_argument("path", nargs="?", type=Path, default=default_root)
    parser.add_argument("--allow-empty", action="store_true", help="allow a repository containing only migration placeholders")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    scan_root = args.path.resolve()
    if not scan_root.is_dir():
        print(f"FAIL file={scan_root} row=0 TC ID=<none> issue=test-case directory does not exist")
        return 1
    seen_ids: dict[str, tuple[Path, int]] = {}
    issues: list[Issue] = []
    rows_found = 0
    for path in sorted(scan_root.rglob("*.md")):
        file_issues, file_rows = validate_file(path, scan_root, seen_ids)
        issues.extend(file_issues)
        rows_found += file_rows
    if not issues and rows_found == 0 and not args.allow_empty:
        print(f"FAIL file={display_path(scan_root, scan_root)} row=0 TC ID=<none> issue=no test cases found; use --allow-empty only during explicit migration")
        return 1
    if not issues:
        print("PASS")
        return 0
    for issue in issues:
        print(f"FAIL file={issue.file} row={issue.row} TC ID={issue.tc_id} issue={issue.message}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
