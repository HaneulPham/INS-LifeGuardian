#!/usr/bin/env python3
"""Validate INS LifeGuardian QA test-case tables in Markdown files."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


REQUIRED_COLUMNS = (
    "TC ID",
    "Priority",
    "Test Area",
    "Title",
    "Preconditions",
    "Test Steps",
    "Expected Result",
    "Expected Integration",
    "Notes",
)
TEST_TABLE_MARKERS = {
    "tc id",
    "test area",
    "preconditions",
    "test steps",
    "expected result",
    "expected integration",
}
ALLOWED_PRIORITIES = ("High", "Medium", "Low", "Lowest")
TC_ID_PATTERN = re.compile(r"^(?:SMAR|MA)-\d+-G\d+-\d{2}$")
NUMBERED_STEP_PATTERN = re.compile(
    r"(?:^|\n|<br\s*/?>)\s*1[.)]\s+\S", re.IGNORECASE
)
VERIFY_MARKER = "**Verify after step"


@dataclass(frozen=True)
class Issue:
    file: Path
    row: int
    tc_id: str
    message: str


def split_markdown_row(line: str) -> list[str]:
    """Split a Markdown table row while preserving escaped pipe characters."""
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
        if character == "\\" and not escaped:
            escaped = True
        else:
            escaped = False
    cells.append("".join(current).strip())
    return [cell.replace(r"\|", "|") for cell in cells]


def is_separator_row(line: str) -> bool:
    cells = split_markdown_row(line)
    return bool(cells) and all(
        re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) is not None
        for cell in cells
    )


def normalize_header(value: str) -> str:
    value = value.replace("`", "").replace("**", "")
    return " ".join(value.split()).casefold()


def is_table_row(line: str) -> bool:
    return "|" in line and bool(line.strip())


def display_path(path: Path, root: Path) -> Path:
    try:
        return path.relative_to(root.parent.parent)
    except ValueError:
        return path


def validate_file(
    path: Path,
    scan_root: Path,
    seen_ids: dict[str, tuple[Path, int]],
) -> list[Issue]:
    issues: list[Issue] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    index = 0

    while index + 1 < len(lines):
        if not is_table_row(lines[index]) or not is_separator_row(lines[index + 1]):
            index += 1
            continue

        headers = split_markdown_row(lines[index])
        normalized_headers = [normalize_header(header) for header in headers]
        if not TEST_TABLE_MARKERS.intersection(normalized_headers):
            index += 2
            continue

        header_map = {
            normalized: position
            for position, normalized in enumerate(normalized_headers)
        }
        missing_columns = [
            column
            for column in REQUIRED_COLUMNS
            if normalize_header(column) not in header_map
        ]
        shown_path = display_path(path, scan_root)
        if missing_columns:
            issues.append(
                Issue(
                    shown_path,
                    index + 1,
                    "<table>",
                    "missing required columns: " + ", ".join(missing_columns),
                )
            )

        row_index = index + 2
        while row_index < len(lines) and is_table_row(lines[row_index]):
            if is_separator_row(lines[row_index]):
                row_index += 1
                continue

            cells = split_markdown_row(lines[row_index])
            if not any(cell.strip() for cell in cells):
                row_index += 1
                continue
            if len(cells) < len(headers):
                cells.extend([""] * (len(headers) - len(cells)))

            def value(column: str) -> str:
                position = header_map.get(normalize_header(column))
                if position is None or position >= len(cells):
                    return ""
                return cells[position].strip()

            tc_id = value("TC ID") or "<missing>"
            source_row = row_index + 1

            if tc_id == "<missing>" or not TC_ID_PATTERN.fullmatch(tc_id):
                issues.append(
                    Issue(shown_path, source_row, tc_id, "invalid TC ID format")
                )

            if tc_id != "<missing>":
                if tc_id in seen_ids:
                    first_file, first_row = seen_ids[tc_id]
                    issues.append(
                        Issue(
                            shown_path,
                            source_row,
                            tc_id,
                            f"duplicate TC ID; first found in {first_file} row {first_row}",
                        )
                    )
                else:
                    seen_ids[tc_id] = (shown_path, source_row)

            priority = value("Priority")
            if priority not in ALLOWED_PRIORITIES:
                allowed = ", ".join(ALLOWED_PRIORITIES)
                issues.append(
                    Issue(
                        shown_path,
                        source_row,
                        tc_id,
                        f"invalid Priority {priority!r}; allowed: {allowed}",
                    )
                )

            test_steps = value("Test Steps")
            if not NUMBERED_STEP_PATTERN.search(test_steps):
                issues.append(
                    Issue(
                        shown_path,
                        source_row,
                        tc_id,
                        "Test Steps must use numbered steps beginning with 1",
                    )
                )

            if VERIFY_MARKER not in value("Expected Result"):
                issues.append(
                    Issue(
                        shown_path,
                        source_row,
                        tc_id,
                        f"Expected Result must contain {VERIFY_MARKER!r}",
                    )
                )

            if VERIFY_MARKER not in value("Expected Integration"):
                issues.append(
                    Issue(
                        shown_path,
                        source_row,
                        tc_id,
                        f"Expected Integration must contain {VERIFY_MARKER!r}",
                    )
                )

            row_index += 1

        index = row_index

    return issues


def parse_args() -> argparse.Namespace:
    default_root = Path(__file__).resolve().parent.parent / "qa-knowledge/test-cases"
    parser = argparse.ArgumentParser(
        description="Validate Markdown QA test cases."
    )
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=default_root,
        help="directory to scan (default: qa-knowledge/test-cases/)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    scan_root = args.path.resolve()
    if not scan_root.is_dir():
        print(
            f"FAIL file={scan_root} row=0 TC ID=<none> "
            "issue=test-case directory does not exist"
        )
        return 1

    markdown_files = sorted(scan_root.rglob("*.md"))
    seen_ids: dict[str, tuple[Path, int]] = {}
    issues: list[Issue] = []
    for path in markdown_files:
        issues.extend(validate_file(path, scan_root, seen_ids))

    if not issues:
        print("PASS")
        return 0

    for issue in issues:
        print(
            f"FAIL file={issue.file} row={issue.row} "
            f"TC ID={issue.tc_id} issue={issue.message}"
        )
    return 1


if __name__ == "__main__":
    sys.exit(main())
