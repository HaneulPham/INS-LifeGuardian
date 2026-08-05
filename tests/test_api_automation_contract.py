from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
API = ROOT / "automation/api"


class ApiAutomationContractTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_api_and_web_are_explicitly_separate(self):
        agents = self.read("AGENTS.md")
        skill = self.read(".agents/skills/ins-lifeguardian-playwright-api-automation/SKILL.md")
        self.assertIn("Web automation is a separate future skill", agents)
        self.assertIn("must not create Web tests", skill)
        self.assertFalse((ROOT / ".agents/skills/ins-lifeguardian-api-automation").exists())

    def test_complete_api_command_chain_is_documented(self):
        commands = self.read(".agents/skills/ins-lifeguardian-qa-analyst/references/workflow-commands.md")
        for command in (
            "write API automation",
            "review API automation",
            "run API automation",
            "debug API automation failure",
            "fix API automation",
            "update API automation mapping",
        ):
            self.assertIn(command, commands)

    def test_framework_scaffold_exists(self):
        for relative in (
            "automation/api/package.json",
            "automation/api/playwright.config.ts",
            "automation/api/tsconfig.json",
            "automation/api/fixtures/api-test.ts",
            "automation/api/clients/base-api.client.ts",
            "automation/api/helpers/traceability.ts",
            "automation/api/mappings/automation-map.json",
            "automation/api/scripts/check-secrets.mjs",
            "automation/api/scripts/check-traceability.mjs",
            "automation/api/scripts/validate-automation.mjs",
        ):
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_framework_uses_request_context_and_no_web_scaffold(self):
        fixture = self.read("automation/api/fixtures/api-test.ts")
        config = self.read("automation/api/playwright.config.ts")
        self.assertIn("playwright.request.newContext", fixture)
        self.assertNotIn("page:", fixture)
        self.assertNotIn("browserName", config)
        self.assertFalse((ROOT / "automation/web").exists())

    def test_environment_rejects_production(self):
        environment = self.read("automation/api/config/environment.ts")
        validator = self.read("automation/api/scripts/validate-environment.mjs")
        self.assertIn("Production API automation is prohibited", environment)
        self.assertIn("Production API automation is prohibited", validator)
        self.assertIn("API_ENVIRONMENT", environment)

    def test_traceability_and_mapping_are_separate_from_manual_status(self):
        helper = self.read("automation/api/helpers/traceability.ts")
        second_brain = self.read("qa-knowledge/automation/api-automation-map.md")
        mapping = json.loads(self.read("automation/api/mappings/automation-map.json"))
        self.assertIn("qa-test-case", helper)
        self.assertIn("`@${metadata.caseId}`", helper)
        self.assertIn("Automation status never", self.read("qa-knowledge/status-glossary.md"))
        self.assertIn("manual test case", second_brain)
        self.assertEqual(1, mapping["schemaVersion"])
        self.assertEqual([], mapping["entries"])

    def test_only_supported_automation_statuses_are_documented(self):
        mapping_reference = self.read(".agents/skills/ins-lifeguardian-playwright-api-automation/references/automation-mapping.md")
        for status in (
            "Candidate",
            "Automated",
            "Partially Automated",
            "Blocked",
            "Not Suitable",
            "Maintenance Required",
        ):
            self.assertIn(status, mapping_reference)

    def test_api_ci_runs_static_validation_without_browser_install(self):
        workflow = self.read(".github/workflows/api-automation-validation.yml")
        self.assertIn("npm install", workflow)
        self.assertIn("npm run validate", workflow)
        self.assertNotIn("playwright install", workflow)
        self.assertIn("PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD", workflow)


if __name__ == "__main__":
    unittest.main()
