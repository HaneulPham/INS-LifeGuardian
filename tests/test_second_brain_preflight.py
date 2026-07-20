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
            flags = "\n".join(f"  {key}: true" for key in sorted(preflight.BOOLEAN_KEYS))
            (root / "qa-knowledge/config.yml").write_text(f"automation:\n{flags}\n  backup_directory: .backups\n", encoding="utf-8")
            (root / ".gitignore").write_text(".backups/\n", encoding="utf-8")
            commands = (
                ("git", "init"),
                ("git", "config", "user.email", "qa@example.invalid"),
                ("git", "config", "user.name", "QA Test"),
                ("git", "add", "."),
                ("git", "commit", "-m", "test fixture"),
            )
            for command in commands:
                subprocess.run(command, cwd=root, check=True, capture_output=True, text=True)
            phrase = "Approve and Update the QA Second Brain for ticket SMAR-100"
            self.assertEqual([], preflight.evaluate(root, phrase, "SMAR-100", [proposal], migration=False))


if __name__ == "__main__":
    unittest.main()
