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


if __name__ == "__main__":
    unittest.main()
