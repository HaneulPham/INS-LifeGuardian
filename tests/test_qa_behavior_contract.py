from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class QABehaviorContractTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_agents_enforces_one_group_and_verify_titles(self):
        text = self.read("AGENTS.md")
        self.assertIn("Write only the requested group", text)
        self.assertIn("plain text beginning with `Verify `", text)
        self.assertIn("Do not bold the entire title", text)
        self.assertIn("Preserve approved IDs", text)

    def test_skill_routes_detailed_cases_to_quality_and_golden_example(self):
        text = self.read(".agents/skills/ins-lifeguardian-qa-analyst/SKILL.md")
        self.assertIn("references/test-case-quality-gate.md", text)
        self.assertIn("references/examples/SMAR-2633-approved-test-case-pattern.md", text)
        self.assertIn("references/reviewer-feedback.md", text)

    def test_detailed_case_references_exist(self):
        for relative in (
            ".agents/skills/ins-lifeguardian-qa-analyst/references/test-case-style.md",
            ".agents/skills/ins-lifeguardian-qa-analyst/references/test-case-quality-gate.md",
            ".agents/skills/ins-lifeguardian-qa-analyst/references/reviewer-feedback.md",
            ".agents/skills/ins-lifeguardian-qa-analyst/references/examples/SMAR-2633-approved-test-case-pattern.md",
        ):
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_golden_example_captures_approved_workflow_order(self):
        text = self.read(".agents/skills/ins-lifeguardian-qa-analyst/references/examples/SMAR-2633-approved-test-case-pattern.md")
        work_orders = text.index("Work Orders → Work Order Management")
        raptor = text.index("Raptor → DVA Submissions")
        self.assertLess(work_orders, raptor)
        self.assertIn("Deferred", text)
        self.assertIn("mixed-batch", text.casefold())
        self.assertIn("next unused ID", text)

    def test_template_uses_verify_title_and_deferred_scenarios(self):
        text = self.read("qa-knowledge/templates/test-case-template.md")
        self.assertIn("Verify <specific observable behaviour>", text)
        self.assertIn("Approved Case Ledger", text)
        self.assertIn("Deferred Scenarios", text)

    def test_reviewer_feedback_has_required_decisions(self):
        text = self.read(".agents/skills/ins-lifeguardian-qa-analyst/references/reviewer-feedback.md")
        for decision in ("Add", "Update", "Merge", "Remove", "Defer", "Reject"):
            self.assertIn(f"**{decision}**", text)

    def test_question_workflow_and_traceability_reference_exist(self):
        self.assertTrue((ROOT / ".agents/skills/ins-lifeguardian-qa-analyst/references/question-decision-workflow.md").is_file())
        intake = self.read(".agents/skills/ins-lifeguardian-qa-analyst/references/requirement-intake.md")
        template = self.read("qa-knowledge/templates/requirement-template.md")
        self.assertIn("Requirement Traceability", intake)
        self.assertIn("Material Behaviour | Source / Evidence | Status", template)

    def test_selectable_questions_and_decision_updates_are_required(self):
        agents = self.read("AGENTS.md")
        workflow = self.read(".agents/skills/ins-lifeguardian-qa-analyst/references/question-decision-workflow.md")
        self.assertIn("one decision per question", agents)
        self.assertIn("Other – specify", workflow)
        self.assertIn("Confirmed Decisions", workflow)
        for decision in ("Add", "Update", "Merge", "Remove", "Defer"):
            self.assertIn(f"**{decision}**", workflow)

    def test_complete_suite_override_is_documented(self):
        agents = self.read("AGENTS.md")
        style = self.read(".agents/skills/ins-lifeguardian-qa-analyst/references/test-case-style.md")
        self.assertIn("explicitly requests all groups", agents)
        self.assertIn("complete suite", style)

    def test_instrumentation_privacy_and_cleanup_are_required(self):
        agents = self.read("AGENTS.md")
        style = self.read(".agents/skills/ins-lifeguardian-qa-analyst/references/test-case-style.md")
        gate = self.read(".agents/skills/ins-lifeguardian-qa-analyst/references/test-case-quality-gate.md")
        self.assertIn("Requires Test Instrumentation", agents)
        self.assertIn("safe cleanup/rollback", style)
        self.assertIn("unnecessary personal, medical, contact, authentication, or tenant data", gate)

    def test_bug_reports_separate_severity_and_priority(self):
        text = self.read(".agents/skills/ins-lifeguardian-qa-analyst/references/bug-report-style.md")
        self.assertIn("- Severity\n- Priority", text)
        self.assertIn("Severity describes", text)
        self.assertIn("Priority describes", text)

    def test_prompt_surfaces_use_selective_loading(self):
        agents = self.read("AGENTS.md")
        skill = self.read(".agents/skills/ins-lifeguardian-qa-analyst/SKILL.md")
        intake = self.read(".agents/skills/ins-lifeguardian-qa-analyst/references/requirement-intake.md")
        self.assertIn("Minimum-context rule", agents)
        self.assertIn("Do not preload the full QA Second Brain", agents)
        self.assertIn("Open only references required", skill)
        self.assertIn("Omit empty sections", intake)
        self.assertNotIn("Read `references/project-scope.md` for every task", skill)

    def test_approved_example_is_conditional_not_mandatory(self):
        skill = self.read(".agents/skills/ins-lifeguardian-qa-analyst/SKILL.md")
        self.assertIn("do not load `references/examples/SMAR-2633-approved-test-case-pattern.md` for every", skill)
        self.assertIn("format uncertainty", skill)

    def test_prompt_file_character_budgets(self):
        limits = {
            "AGENTS.md": 7600,
            ".agents/skills/ins-lifeguardian-qa-analyst/SKILL.md": 7800,
            ".agents/skills/ins-lifeguardian-qa-analyst/references/requirement-intake.md": 4200,
            ".agents/skills/ins-lifeguardian-qa-analyst/references/test-case-style.md": 6500,
        }
        for relative, limit in limits.items():
            self.assertLessEqual(len(self.read(relative)), limit, relative)

    def test_canonical_workflow_commands_and_suggestions_are_enforced(self):
        agents = self.read("AGENTS.md")
        commands = self.read(".agents/skills/ins-lifeguardian-qa-analyst/references/workflow-commands.md")
        for command in (
            "analytics",
            "write test cases",
            "review test cases",
            "Update test cases to Second Brain",
            "write a bug",
            "write API automation",
            "review API automation",
            "run API automation",
            "debug API automation failure",
            "fix API automation",
            "update API automation mapping",
        ):
            self.assertIn(command, agents)
            self.assertIn(command, commands)
        self.assertIn("Suggested next command:", agents)
        self.assertIn("at most one", commands)
        self.assertIn("direct execution command", commands)
        self.assertIn("do not require a second approval phrase", commands)

    def test_second_brain_command_is_direct_and_confluence_backed(self):
        agents = self.read("AGENTS.md")
        analyst = self.read(".agents/skills/ins-lifeguardian-qa-analyst/SKILL.md")
        librarian = self.read(".agents/skills/ins-lifeguardian-qa-librarian/SKILL.md")
        template = self.read("qa-knowledge/templates/update-second-brain-prompt.md")
        for text in (agents, analyst, librarian, template):
            self.assertIn("Update test cases to Second Brain", text)
        self.assertIn("direct write authorization", agents)
        self.assertIn("route directly to the Librarian", analyst)
        self.assertIn("supplied Confluence", librarian)
        self.assertIn("No second approval phrase", template)
        self.assertNotIn("Approve and Update the QA Second Brain", agents)

    def test_direct_update_config_preserves_conflicts_without_blocking_valid_work(self):
        config = self.read("qa-knowledge/config.yml")
        self.assertIn("stop_on_conflict: false", config)
        librarian = self.read(".agents/skills/ins-lifeguardian-qa-librarian/SKILL.md")
        self.assertIn("Preserve evidence-backed Conflict/GAP records", librarian)

    def test_api_automation_is_progressively_disclosed_and_safe(self):
        agents = self.read("AGENTS.md")
        analyst = self.read(".agents/skills/ins-lifeguardian-qa-analyst/SKILL.md")
        api_skill = self.read(".agents/skills/ins-lifeguardian-playwright-api-automation/SKILL.md")
        self.assertIn("ins-lifeguardian-playwright-api-automation", agents)
        self.assertIn("route to `ins-lifeguardian-playwright-api-automation`", analyst)
        self.assertIn("Do not invent endpoints", api_skill)
        self.assertIn("environment variables", api_skill)
        self.assertIn("Could Not Automate", api_skill)
        self.assertIn("Do not add dependencies or a second framework silently", api_skill)
        self.assertIn("must not create Web tests", api_skill)

    def test_workflow_prompt_templates_exist(self):
        for relative in (
            "qa-knowledge/templates/analytics-prompt.md",
            "qa-knowledge/templates/write-test-case-group-prompt.md",
            "qa-knowledge/templates/review-test-cases-prompt.md",
            "qa-knowledge/templates/update-second-brain-prompt.md",
            "qa-knowledge/templates/write-bug-prompt.md",
            "qa-knowledge/templates/write-api-automation-prompt.md",
        ):
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_only_high_medium_low_are_documented_priorities(self):
        for relative in (
            ".agents/skills/ins-lifeguardian-qa-analyst/references/requirement-review.md",
            ".agents/skills/ins-lifeguardian-qa-analyst/references/test-case-style.md",
            ".agents/skills/ins-lifeguardian-qa-analyst/references/test-case-quality-gate.md",
        ):
            text = self.read(relative)
            self.assertNotIn("Lowest", text, relative)


if __name__ == "__main__":
    unittest.main()
