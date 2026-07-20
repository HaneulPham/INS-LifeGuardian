from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import validate_qa_knowledge as knowledge  # noqa: E402
import validate_qa_test_cases as cases  # noqa: E402


UI_HEADER = "| TC ID | Priority | Test Area | Title | Preconditions | Test Steps | Expected Result | Expected Integration | Notes |"
UI_SEPARATOR = "|---|---|---|---|---|---|---|---|---|"
API_HEADER = "| TC ID | Priority | API Endpoint | Method | Title | Preconditions | Request Data | Expected Response | Notes |"
API_SEPARATOR = UI_SEPARATOR
REGRESSION_HEADER = "| ID | Priority | Test Area | Summary | Preconditions | Test Steps | Check on CP | Check on Portal | Integration Check |"
REGRESSION_SEPARATOR = UI_SEPARATOR


def ui_row(tc_id: str = "SMAR-100-G1-01", priority: str = "High", expected_step: int = 1) -> str:
    marker = f"**Verify after step #{expected_step}:** result"
    return f"| {tc_id} | {priority} | Area | A \\| B | Ready | 1. Act<br>2. Observe | {marker} | {marker} | None |"


class TestCaseValidatorTests(unittest.TestCase):
    def validate(self, filename: str, text: str):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / filename
            path.write_text(text, encoding="utf-8")
            return cases.validate_file(path, root, {})

    def test_valid_ui_table_with_escaped_pipe_and_br_steps(self):
        issues, count = self.validate("SMAR-100.md", "\n".join((UI_HEADER, UI_SEPARATOR, ui_row())))
        self.assertEqual([], issues)
        self.assertEqual(1, count)

    def test_valid_api_table(self):
        row = "| SMAR-100-G2-01 | Medium | /tasks | POST | Create task | Authenticated | `{}` | 201 response | None |"
        issues, _ = self.validate("SMAR-100.md", "\n".join((API_HEADER, API_SEPARATOR, row)))
        self.assertEqual([], issues)

    def test_valid_regression_table(self):
        marker = "**Verify after step #1:** unchanged"
        row = f"| SMAR-100-G3-01 | Low | Tasks | Regression | Existing task | 1. Open task | {marker} | {marker} | {marker} |"
        issues, _ = self.validate("SMAR-100.md", "\n".join((REGRESSION_HEADER, REGRESSION_SEPARATOR, row)))
        self.assertEqual([], issues)

    def test_duplicate_ids_are_rejected(self):
        text = "\n".join((UI_HEADER, UI_SEPARATOR, ui_row(), ui_row()))
        issues, _ = self.validate("SMAR-100.md", text)
        self.assertTrue(any("duplicate TC ID" in issue.message for issue in issues))

    def test_invalid_priority_is_rejected(self):
        issues, _ = self.validate("SMAR-100.md", "\n".join((UI_HEADER, UI_SEPARATOR, ui_row(priority="Critical"))))
        self.assertTrue(any("invalid Priority" in issue.message for issue in issues))

    def test_incorrect_ticket_prefix_is_rejected(self):
        issues, _ = self.validate("SMAR-100.md", "\n".join((UI_HEADER, UI_SEPARATOR, ui_row(tc_id="MA-100-G1-01"))))
        self.assertTrue(any("prefix must match" in issue.message for issue in issues))

    def test_missing_step_reference_is_rejected(self):
        issues, _ = self.validate("SMAR-100.md", "\n".join((UI_HEADER, UI_SEPARATOR, ui_row(expected_step=3))))
        self.assertTrue(any("references missing step" in issue.message for issue in issues))

    def test_missing_expected_response_is_rejected(self):
        row = "| SMAR-100-G2-01 | Medium | /tasks | POST | Create task | Authenticated | `{}` | | None |"
        issues, _ = self.validate("SMAR-100.md", "\n".join((API_HEADER, API_SEPARATOR, row)))
        self.assertTrue(any("Expected Response must not be empty" in issue.message for issue in issues))


class KnowledgeValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for relative in (
            "qa-knowledge/requirements/SMAR",
            "qa-knowledge/test-cases/SMAR",
            "qa-knowledge/product/modules",
            "qa-knowledge/decisions",
            "qa-knowledge/regression",
        ):
            (self.root / relative).mkdir(parents=True, exist_ok=True)
        (self.root / "qa-knowledge/decisions/decision-log.md").write_text("# Decisions\n", encoding="utf-8")
        (self.root / "qa-knowledge/regression/regression-map.md").write_text("# Regression\n", encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def requirement(self, status: str = "Confirmed", extra: str = "") -> str:
        return (
            "# Requirement\n\n## Confirmed Decisions\nNone\n\n## Regression Risk\nNone\n\n"
            "## Knowledge Status\n\n"
            "| Knowledge Item | Source Status | Source / Evidence | Last Updated | Notes |\n"
            "|---|---|---|---|---|\n"
            f"| Rule | {status} | Ticket | 2026-07-20 | Note |\n{extra}"
        )

    def write_index(self, status: str = "Pending Migration", requirement: str = "requirements/SMAR/SMAR-100.md", test_case: str = "test-cases/SMAR/SMAR-100.md"):
        (self.root / "qa-knowledge/ticket-index.md").write_text(
            "| Ticket | Requirement File | Test Case File | Status |\n|---|---|---|---|\n"
            f"| SMAR-100 | {requirement} | {test_case} | {status} |\n",
            encoding="utf-8",
        )

    def test_unsupported_source_status(self):
        path = self.root / "qa-knowledge/requirements/SMAR/SMAR-100.md"
        path.write_text(self.requirement("Maybe"), encoding="utf-8")
        issues = knowledge.validate_knowledge_status_files(self.root)
        self.assertTrue(any("unsupported Source Status" in issue.message for issue in issues))

    def test_missing_indexed_files(self):
        self.write_index()
        issues = knowledge.validate_ticket_index(self.root)
        self.assertEqual(2, sum("does not exist" in issue.message for issue in issues))

    def test_completed_placeholder_is_rejected(self):
        requirement = self.root / "qa-knowledge/requirements/SMAR/SMAR-100.md"
        test_case = self.root / "qa-knowledge/test-cases/SMAR/SMAR-100.md"
        requirement.write_text(self.requirement(extra="\nPending Migration\n"), encoding="utf-8")
        test_case.write_text("# Cases\n\nPending Migration\n", encoding="utf-8")
        self.write_index("Completed")
        issues = knowledge.validate_ticket_index(self.root)
        self.assertTrue(any("migration placeholder" in issue.message for issue in issues))

    def test_decision_and_regression_log_enforcement(self):
        requirement = self.root / "qa-knowledge/requirements/SMAR/SMAR-100.md"
        test_case = self.root / "qa-knowledge/test-cases/SMAR/SMAR-100.md"
        requirement.write_text(self.requirement().replace("## Confirmed Decisions\nNone", "## Confirmed Decisions\nA decision").replace("## Regression Risk\nNone", "## Regression Risk\nA risk"), encoding="utf-8")
        marker = "**Verify after step #1:** result"
        test_case.write_text("\n".join(("# Cases", "", "## Group 1", "", UI_HEADER, UI_SEPARATOR, f"| SMAR-100-G1-01 | High | Area | Title | Ready | 1. Act | {marker} | {marker} | None |")), encoding="utf-8")
        self.write_index("Completed")
        issues = knowledge.validate_ticket_index(self.root)
        self.assertTrue(any("decision log" in issue.message for issue in issues))
        self.assertTrue(any("regression map" in issue.message for issue in issues))


if __name__ == "__main__":
    unittest.main()
