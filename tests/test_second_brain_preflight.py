from __future__ import annotations

import sys
import subprocess
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import second_brain_preflight as preflight  # noqa: E402


class PreflightTests(unittest.TestCase):
    def initialize_git(self, root: Path):
        commands = (
            ("git", "init"),
            ("git", "config", "user.email", "qa@example.invalid"),
            ("git", "config", "user.name", "QA Test"),
            ("git", "add", "."),
            ("git", "commit", "-m", "test fixture"),
        )
        for command in commands:
            subprocess.run(command, cwd=root, check=True, capture_output=True, text=True)

    def write_config(self, root: Path):
        flags = "\n".join(f"  {key}: true" for key in sorted(preflight.BOOLEAN_KEYS))
        (root / "qa-knowledge").mkdir(parents=True, exist_ok=True)
        (root / "qa-knowledge/config.yml").write_text(f"automation:\n{flags}\n  backup_directory: .backups\n", encoding="utf-8")
        (root / ".gitignore").write_text(".backups/\n", encoding="utf-8")

    def test_config_requires_boolean_flags(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.yml"
            path.write_text("automation:\n  auto_apply_second_brain_updates: yes\n  backup_directory: .backups\n", encoding="utf-8")
            _, issues = preflight.load_automation_config(path)
            self.assertTrue(any("must be true or false" in issue for issue in issues))
            self.assertTrue(any("missing automation setting" in issue for issue in issues))

    def test_sensitive_content_is_blocked_without_echoing_value(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "proposal.md"
            secret = "super-secret-value"
            path.write_text(f"API key: {secret}\n", encoding="utf-8")
            issues = preflight.inspect_sensitive_text([path])
            self.assertTrue(any("credential or secret" in issue for issue in issues))
            self.assertFalse(any(secret in issue for issue in issues))

    def test_iso_date_is_not_treated_as_phone_number(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "proposal.md"
            path.write_text("Last Updated: 2026-07-20\n", encoding="utf-8")
            self.assertEqual([], preflight.inspect_sensitive_text([path]))

    def test_clean_repository_passes_full_evaluation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            requirement = root / "qa-knowledge/requirements/SMAR/SMAR-100.md"
            test_cases = root / "qa-knowledge/test-cases/SMAR/SMAR-100.md"
            requirement.parent.mkdir(parents=True)
            test_cases.parent.mkdir(parents=True)
            requirement.write_text("# Approved requirement\n", encoding="utf-8")
            test_cases.write_text("# Approved cases\n", encoding="utf-8")
            proposal = root / "proposal.md"
            proposal.write_text("Sanitized approved content\n", encoding="utf-8")
            self.write_config(root)
            self.initialize_git(root)
            phrase = "Update test cases to Second Brain"
            self.assertEqual([], preflight.evaluate(root, phrase, "SMAR-100", [proposal], migration=False))

    def test_create_ticket_mode_accepts_new_ticket_with_templates(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in (
                "qa-knowledge/requirements",
                "qa-knowledge/test-cases",
                "qa-knowledge/templates",
            ):
                (root / relative).mkdir(parents=True, exist_ok=True)
            (root / "qa-knowledge/templates/requirement-template.md").write_text("# <Ticket ID>\n", encoding="utf-8")
            (root / "qa-knowledge/templates/test-case-template.md").write_text("# <Ticket ID>\n", encoding="utf-8")
            (root / "qa-knowledge/ticket-index.md").write_text("| Ticket |\n|---|\n", encoding="utf-8")
            proposal = root / "proposal.md"
            proposal.write_text("Sanitized approved content\n", encoding="utf-8")
            self.write_config(root)
            self.initialize_git(root)
            phrase = "Update test cases to Second Brain"
            issues = preflight.evaluate(root, phrase, "SMAR-3000", [proposal], migration=False, create_ticket=True)
            self.assertEqual([], issues)
            requirement, test_cases = preflight.ticket_paths(root, "SMAR-3000")
            self.assertFalse(requirement.exists())
            self.assertFalse(test_cases.exists())

    def test_create_ticket_mode_rejects_existing_index_entry(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in (
                "qa-knowledge/requirements",
                "qa-knowledge/test-cases",
                "qa-knowledge/templates",
            ):
                (root / relative).mkdir(parents=True, exist_ok=True)
            (root / "qa-knowledge/templates/requirement-template.md").write_text("template\n", encoding="utf-8")
            (root / "qa-knowledge/templates/test-case-template.md").write_text("template\n", encoding="utf-8")
            (root / "qa-knowledge/ticket-index.md").write_text("| Ticket |\n|---|\n| SMAR-3000 |\n", encoding="utf-8")
            proposal = root / "proposal.md"
            proposal.write_text("Sanitized approved content\n", encoding="utf-8")
            self.write_config(root)
            self.initialize_git(root)
            phrase = "Update test cases to Second Brain"
            issues = preflight.evaluate(root, phrase, "SMAR-3000", [proposal], migration=False, create_ticket=True)
            self.assertTrue(any("already exists" in issue for issue in issues))

    def test_direct_command_phrase_is_case_insensitive(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            requirement = root / "qa-knowledge/requirements/SMAR/SMAR-104.md"
            test_cases = root / "qa-knowledge/test-cases/SMAR/SMAR-104.md"
            requirement.parent.mkdir(parents=True)
            test_cases.parent.mkdir(parents=True)
            requirement.write_text("# Requirement\n", encoding="utf-8")
            test_cases.write_text("# Cases\n", encoding="utf-8")
            proposal = root / "proposal.md"
            proposal.write_text("Reviewed content\n", encoding="utf-8")
            self.write_config(root)
            self.initialize_git(root)
            issues = preflight.evaluate(root, "update test cases to second brain", "SMAR-104", [proposal], migration=False)
            self.assertEqual([], issues)

    def test_old_two_step_approval_phrase_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            requirement = root / "qa-knowledge/requirements/SMAR/SMAR-101.md"
            test_cases = root / "qa-knowledge/test-cases/SMAR/SMAR-101.md"
            requirement.parent.mkdir(parents=True)
            test_cases.parent.mkdir(parents=True)
            requirement.write_text("# Requirement\n", encoding="utf-8")
            test_cases.write_text("# Cases\n", encoding="utf-8")
            proposal = root / "proposal.md"
            proposal.write_text("Reviewed content\n", encoding="utf-8")
            self.write_config(root)
            self.initialize_git(root)
            issues = preflight.evaluate(
                root,
                "Approve and Update the QA Second Brain for ticket SMAR-101",
                "SMAR-101",
                [proposal],
                migration=False,
            )
            self.assertTrue(any("direct update command phrase" in issue for issue in issues))

    def test_existing_conflict_does_not_block_unrelated_reviewed_update(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            requirement = root / "qa-knowledge/requirements/SMAR/SMAR-102.md"
            test_cases = root / "qa-knowledge/test-cases/SMAR/SMAR-102.md"
            requirement.parent.mkdir(parents=True)
            test_cases.parent.mkdir(parents=True)
            requirement.write_text("| Rule | Conflict |\n", encoding="utf-8")
            test_cases.write_text("# Cases\n", encoding="utf-8")
            proposal = root / "proposal.md"
            proposal.write_text("Reviewed unrelated valid case\n", encoding="utf-8")
            self.write_config(root)
            self.initialize_git(root)
            issues = preflight.evaluate(root, "Update test cases to Second Brain", "SMAR-102", [proposal], migration=False)
            self.assertEqual([], issues)

    def test_proposed_conflict_is_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            requirement = root / "qa-knowledge/requirements/SMAR/SMAR-103.md"
            test_cases = root / "qa-knowledge/test-cases/SMAR/SMAR-103.md"
            requirement.parent.mkdir(parents=True)
            test_cases.parent.mkdir(parents=True)
            requirement.write_text("# Requirement\n", encoding="utf-8")
            test_cases.write_text("# Cases\n", encoding="utf-8")
            proposal = root / "proposal.md"
            proposal.write_text("| Rule | Conflict |\n", encoding="utf-8")
            self.write_config(root)
            self.initialize_git(root)
            issues = preflight.evaluate(root, "Update test cases to Second Brain", "SMAR-103", [proposal], migration=False)
            self.assertTrue(any("proposed content contains unresolved Conflict" in issue for issue in issues))


if __name__ == "__main__":
    unittest.main()
