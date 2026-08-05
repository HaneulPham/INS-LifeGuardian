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
SEPARATOR = "|---|---|---|---|---|---|---|---|---|"
API_HEADER = "| TC ID | Priority | API Endpoint | Method | Title | Preconditions | Request Data | Expected Response | Notes |"
REGRESSION_HEADER = "| ID | Priority | Test Area | Summary | Preconditions | Test Steps | Check on CP | Check on Portal | Integration Check |"


def ui_row(
    tc_id: str = "SMAR-100-G1-01",
    priority: str = "High",
    expected_step: int = 3,
    test_area: str = "Service Requests > Type",
    title: str = "Verify Billing service request type is selectable",
    steps: str = "1. Log in to CP Web<br>2. Navigate to Service Requests<br>3. Select Create",
    expected_result: str | None = None,
    expected_integration: str | None = None,
) -> str:
    result = expected_result or f"**Verify after step #{expected_step}:** Billing is available exactly once"
    integration = expected_integration or f"**Verify after step #{expected_step}:** No notification integration is triggered"
    return f"| {tc_id} | {priority} | {test_area} | {title} | Authorized user | {steps} | {result} | {integration} | None |"


class TestCaseValidatorTests(unittest.TestCase):
    def validate(self, filename: str, text: str):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / filename
            path.write_text(text, encoding="utf-8")
            return cases.validate_file(path, root, {}, {})

    def ui_table(self, *rows: str, group: int = 1) -> str:
        return "\n".join((f"## Group {group}", "", UI_HEADER, SEPARATOR, *rows))

    def test_valid_ui_table_with_escaped_pipe_and_br_steps(self):
        row = ui_row(title="Verify Billing \\| manual service request type is selectable")
        issues, count = self.validate("SMAR-100.md", self.ui_table(row))
        self.assertEqual([], issues)
        self.assertEqual(1, count)

    def test_valid_api_table(self):
        row = "| SMAR-100-G2-01 | Medium | /tasks | POST | Verify care plan task is created | Authenticated | `{}` | 201 response contains the created task identifier | None |"
        issues, _ = self.validate("SMAR-100.md", "\n".join(("## Group 2", "", API_HEADER, SEPARATOR, row)))
        self.assertEqual([], issues)

    def test_valid_regression_table(self):
        marker = "**Verify after step #2:** task state remains unchanged"
        row = f"| SMAR-100-G3-01 | Low | Care Plan Tasks > Synchronization | Verify task synchronization | Existing task | 1. Open Task List<br>2. Refresh tasks | {marker} | {marker} | {marker} |"
        issues, _ = self.validate("SMAR-100.md", "\n".join(("## Group 3", "", REGRESSION_HEADER, SEPARATOR, row)))
        self.assertEqual([], issues)

    def test_duplicate_ids_are_rejected(self):
        issues, _ = self.validate("SMAR-100.md", self.ui_table(ui_row(), ui_row()))
        self.assertTrue(any("duplicate TC ID" in issue.message for issue in issues))

    def test_invalid_priority_is_rejected(self):
        issues, _ = self.validate("SMAR-100.md", self.ui_table(ui_row(priority="Critical")))
        self.assertTrue(any("invalid Priority" in issue.message for issue in issues))

    def test_lowest_priority_is_rejected(self):
        issues, _ = self.validate("SMAR-100.md", self.ui_table(ui_row(priority="Lowest")))
        self.assertTrue(any("invalid Priority" in issue.message for issue in issues))
        self.assertTrue(any("allowed: High, Medium, Low" in issue.message for issue in issues))

    def test_incorrect_ticket_prefix_is_rejected(self):
        issues, _ = self.validate("SMAR-100.md", self.ui_table(ui_row(tc_id="MA-100-G1-01")))
        self.assertTrue(any("prefix must match" in issue.message for issue in issues))

    def test_group_heading_and_id_mismatch_is_rejected(self):
        issues, _ = self.validate("SMAR-100.md", self.ui_table(ui_row(tc_id="SMAR-100-G9-01"), group=1))
        self.assertTrue(any("group must match Group 1" in issue.message for issue in issues))

    def test_missing_step_reference_is_rejected(self):
        issues, _ = self.validate("SMAR-100.md", self.ui_table(ui_row(expected_step=4)))
        self.assertTrue(any("references missing step" in issue.message for issue in issues))

    def test_missing_step_number_is_rejected(self):
        row = ui_row(steps="1. Open Service Requests<br>3. Select Create", expected_step=3)
        issues, _ = self.validate("SMAR-100.md", self.ui_table(row))
        self.assertTrue(any("complete, non-duplicated sequence" in issue.message for issue in issues))

    def test_duplicate_step_number_is_rejected(self):
        row = ui_row(steps="1. Open Service Requests<br>1. Select Create", expected_step=1)
        issues, _ = self.validate("SMAR-100.md", self.ui_table(row))
        self.assertTrue(any("complete, non-duplicated sequence" in issue.message for issue in issues))

    def test_first_case_without_full_navigation_is_rejected(self):
        row = ui_row(steps="1. Select Billing", expected_step=1)
        issues, _ = self.validate("SMAR-100.md", self.ui_table(row))
        self.assertTrue(any("full navigation flow" in issue.message for issue in issues))

    def test_first_case_with_multiple_steps_but_no_navigation_is_rejected(self):
        row = ui_row(steps="1. Select Billing<br>2. Save request", expected_step=2)
        issues, _ = self.validate("SMAR-100.md", self.ui_table(row))
        self.assertTrue(any("full navigation flow" in issue.message for issue in issues))

    def test_broad_test_area_is_rejected(self):
        issues, _ = self.validate("SMAR-100.md", self.ui_table(ui_row(test_area="General")))
        self.assertTrue(any("too broad" in issue.message for issue in issues))

    def test_vague_expected_result_is_rejected(self):
        row = ui_row(expected_result="**Verify after step #2:** Works correctly")
        issues, _ = self.validate("SMAR-100.md", self.ui_table(row))
        self.assertTrue(any("Expected Result contains vague phrase" in issue.message for issue in issues))

    def test_vague_title_is_rejected(self):
        row = ui_row(title="Feature works correctly")
        issues, _ = self.validate("SMAR-100.md", self.ui_table(row))
        self.assertTrue(any("Title contains vague phrase" in issue.message for issue in issues))

    def test_vague_expected_integration_is_rejected(self):
        row = ui_row(expected_integration="**Verify after step #2:** Works as expected")
        issues, _ = self.validate("SMAR-100.md", self.ui_table(row))
        self.assertTrue(any("Expected Integration contains vague phrase" in issue.message for issue in issues))

    def test_duplicate_normalized_titles_are_rejected(self):
        first = ui_row(title="Verify Billing can be selected")
        second = ui_row(tc_id="SMAR-100-G1-02", title="Verify billing can be selected.")
        issues, _ = self.validate("SMAR-100.md", self.ui_table(first, second))
        self.assertTrue(any("potential duplicate title" in issue.message for issue in issues))

    def test_ui_title_must_begin_with_verify(self):
        issues, _ = self.validate("SMAR-100.md", self.ui_table(ui_row(title="Billing service request type is selectable")))
        self.assertTrue(any("Title must begin with 'Verify '" in issue.message for issue in issues))

    def test_api_title_must_begin_with_verify(self):
        row = "| SMAR-100-G2-01 | Medium | /tasks | POST | Care plan task is created | Authenticated | `{}` | 201 response contains the created task identifier | None |"
        issues, _ = self.validate("SMAR-100.md", "\n".join(("## Group 2", "", API_HEADER, SEPARATOR, row)))
        self.assertTrue(any("Title must begin with 'Verify '" in issue.message for issue in issues))

    def test_fully_bold_title_is_rejected(self):
        issues, _ = self.validate("SMAR-100.md", self.ui_table(ui_row(title="**Verify Billing is selectable**")))
        self.assertTrue(any("do not bold the entire title" in issue.message for issue in issues))

    def test_steps_must_not_depend_on_previous_case(self):
        row = ui_row(steps="1. Continue from the previous case<br>2. Navigate to Service Requests<br>3. Select Create")
        issues, _ = self.validate("SMAR-100.md", self.ui_table(row))
        self.assertTrue(any("independently reproducible" in issue.message for issue in issues))

    def test_invalid_api_method_is_rejected(self):
        row = "| SMAR-100-G2-01 | High | /tasks | BANANA | Verify care plan task is created | Authenticated | `{}` | 200 response contains task data | None |"
        issues, _ = self.validate("SMAR-100.md", "\n".join(("## Group 2", "", API_HEADER, SEPARATOR, row)))
        self.assertTrue(any("invalid HTTP method" in issue.message for issue in issues))

    def test_api_response_without_status_code_is_rejected(self):
        row = "| SMAR-100-G2-01 | High | /tasks | POST | Verify care plan task is created | Authenticated | `{}` | response contains task data | None |"
        issues, _ = self.validate("SMAR-100.md", "\n".join(("## Group 2", "", API_HEADER, SEPARATOR, row)))
        self.assertTrue(any("must include an HTTP status code" in issue.message for issue in issues))

    def test_vague_api_response_is_rejected(self):
        row = "| SMAR-100-G2-01 | High | /tasks | POST | Verify care plan task is created | Authenticated | `{}` | 200 success | None |"
        issues, _ = self.validate("SMAR-100.md", "\n".join(("## Group 2", "", API_HEADER, SEPARATOR, row)))
        self.assertTrue(any("Expected Response contains vague phrase" in issue.message for issue in issues))

    def test_negative_api_response_requires_error_expectation(self):
        row = "| SMAR-100-G2-01 | High | /tasks | POST | Verify invalid task request is rejected | Authenticated | `{}` | 400 response | None |"
        issues, _ = self.validate("SMAR-100.md", "\n".join(("## Group 2", "", API_HEADER, SEPARATOR, row)))
        self.assertTrue(any("negative Expected Response" in issue.message for issue in issues))


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
            "# SMAR-100 — Requirement\n\n## Confirmed Decisions\nNone\n\n## Regression Risk\nNone\n\n"
            "## Knowledge Status\n\n"
            "| Knowledge Item | Source Status | Source / Evidence | Last Updated | Notes |\n"
            "|---|---|---|---|---|\n"
            f"| Rule | {status} | Ticket | 2026-07-20 | Note |\n{extra}"
        )

    def write_index(self, status: str = "Pending Migration", requirement: str = "requirements/SMAR/SMAR-100.md", test_case: str = "test-cases/SMAR/SMAR-100.md", rows: int = 1):
        data_row = f"| SMAR-100 | {requirement} | {test_case} | {status} |\n"
        (self.root / "qa-knowledge/ticket-index.md").write_text(
            "| Ticket | Requirement File | Test Case File | Status |\n|---|---|---|---|\n" + data_row * rows,
            encoding="utf-8",
        )

    def write_ticket_files(self, test_text: str = "# SMAR-100 — Approved Test Cases\n"):
        (self.root / "qa-knowledge/requirements/SMAR/SMAR-100.md").write_text(self.requirement(), encoding="utf-8")
        (self.root / "qa-knowledge/test-cases/SMAR/SMAR-100.md").write_text(test_text, encoding="utf-8")

    def test_unsupported_source_status(self):
        path = self.root / "qa-knowledge/requirements/SMAR/SMAR-100.md"
        path.write_text(self.requirement("Maybe"), encoding="utf-8")
        issues = knowledge.validate_knowledge_status_files(self.root)
        self.assertTrue(any("unsupported Source Status" in issue.message for issue in issues))

    def test_missing_indexed_files(self):
        self.write_index()
        issues = knowledge.validate_ticket_index(self.root)
        self.assertEqual(2, sum("does not exist" in issue.message for issue in issues))

    def test_duplicate_ticket_index_rows(self):
        self.write_ticket_files()
        self.write_index(rows=2)
        issues = knowledge.validate_ticket_index(self.root)
        self.assertTrue(any("duplicate ticket row" in issue.message for issue in issues))

    def test_unsupported_ticket_index_status(self):
        self.write_ticket_files()
        self.write_index(status="Almost Done")
        issues = knowledge.validate_ticket_index(self.root)
        self.assertTrue(any("unsupported ticket status" in issue.message for issue in issues))

    def test_invalid_ticket_id_is_rejected(self):
        self.write_ticket_files()
        self.write_index()
        index_path = self.root / "qa-knowledge/ticket-index.md"
        index_path.write_text(index_path.read_text(encoding="utf-8").replace("SMAR-100", "TICKET-100", 1), encoding="utf-8")
        issues = knowledge.validate_ticket_index(self.root)
        self.assertTrue(any("invalid ticket ID format" in issue.message for issue in issues))

    def test_completed_placeholder_is_rejected(self):
        self.write_ticket_files("# SMAR-100 — Approved Test Cases\n\nPending Migration\n")
        requirement = self.root / "qa-knowledge/requirements/SMAR/SMAR-100.md"
        requirement.write_text(self.requirement(extra="\nPending Migration\n"), encoding="utf-8")
        self.write_index("Completed")
        issues = knowledge.validate_ticket_index(self.root)
        self.assertTrue(any("migration placeholder" in issue.message for issue in issues))

    def test_completed_ticket_with_incorrect_case_id_is_rejected(self):
        marker = "**Verify after step #2:** specific result"
        test_text = "\n".join(("# SMAR-100 — Approved Test Cases", "", "## Group 1", "", UI_HEADER, SEPARATOR, f"| MA-999-G1-01 | High | Tasks > Create | Verify task creation | Ready | 1. Open Tasks<br>2. Select Create | {marker} | {marker} | None |"))
        self.write_ticket_files(test_text)
        self.write_index("Completed")
        issues = knowledge.validate_ticket_index(self.root)
        self.assertTrue(any("incorrect ticket ID" in issue.message for issue in issues))

    def test_filename_must_match_ticket(self):
        self.write_ticket_files()
        self.write_index(requirement="requirements/SMAR/SMAR-999.md")
        issues = knowledge.validate_ticket_index(self.root)
        self.assertTrue(any("requirement filename must match" in issue.message for issue in issues))

    def test_test_case_filename_must_match_ticket(self):
        self.write_ticket_files()
        self.write_index(test_case="test-cases/SMAR/SMAR-999.md")
        issues = knowledge.validate_ticket_index(self.root)
        self.assertTrue(any("test-case filename must match" in issue.message for issue in issues))

    def test_heading_must_match_ticket(self):
        self.write_ticket_files()
        (self.root / "qa-knowledge/requirements/SMAR/SMAR-100.md").write_text("# Wrong heading\n", encoding="utf-8")
        self.write_index()
        issues = knowledge.validate_ticket_index(self.root)
        self.assertTrue(any("heading must begin" in issue.message for issue in issues))

    def test_orphan_requirement_and_case_files_are_rejected(self):
        self.write_index()
        orphan_requirement = self.root / "qa-knowledge/requirements/SMAR/SMAR-999.md"
        orphan_case = self.root / "qa-knowledge/test-cases/SMAR/SMAR-999.md"
        orphan_requirement.write_text("# SMAR-999\n", encoding="utf-8")
        orphan_case.write_text("# SMAR-999\n", encoding="utf-8")
        issues = knowledge.validate_ticket_index(self.root)
        self.assertTrue(any("requirement file has no ticket-index entry" in issue.message for issue in issues))
        self.assertTrue(any("test-case file has no ticket-index entry" in issue.message for issue in issues))

    def test_decision_and_regression_log_enforcement(self):
        marker = "**Verify after step #2:** specific result"
        test_text = "\n".join(("# SMAR-100 — Approved Test Cases", "", "## Group 1", "", UI_HEADER, SEPARATOR, f"| SMAR-100-G1-01 | High | Tasks > Create | Verify task creation | Ready | 1. Open Tasks<br>2. Select Create | {marker} | {marker} | None |"))
        self.write_ticket_files(test_text)
        requirement = self.root / "qa-knowledge/requirements/SMAR/SMAR-100.md"
        requirement.write_text(self.requirement().replace("## Confirmed Decisions\nNone", "## Confirmed Decisions\nA decision").replace("## Regression Risk\nNone", "## Regression Risk\nA risk"), encoding="utf-8")
        self.write_index("Completed")
        issues = knowledge.validate_ticket_index(self.root)
        self.assertTrue(any("decision log" in issue.message for issue in issues))
        self.assertTrue(any("regression map" in issue.message for issue in issues))


class RepositoryConfigurationTests(unittest.TestCase):
    def test_ci_uses_strict_validation(self):
        workflow = (PROJECT_ROOT / ".github/workflows/qa-validation.yml").read_text(encoding="utf-8")
        self.assertNotIn("--allow-empty", workflow)
        self.assertNotIn("QA_MIGRATION_MODE", workflow)
        self.assertIn("python3 scripts/validate_qa_test_cases.py", workflow)

    def test_codex_environment_defaults_to_strict_validation(self):
        environment = (PROJECT_ROOT / ".codex/environments/environment.toml").read_text(encoding="utf-8")
        self.assertIn('${QA_MIGRATION_MODE:-false}', environment)
        self.assertIn('echo "Running strict QA validation..."', environment)
        self.assertEqual(1, environment.count("--allow-empty"))

    def test_atlassian_is_optional_for_offline_repository_work(self):
        config = (PROJECT_ROOT / ".codex/config.toml").read_text(encoding="utf-8")
        self.assertIn("required = false", config)


if __name__ == "__main__":
    unittest.main()
