# Write One Detailed Test-Case Group

```text
Use the active INS LifeGuardian ticket context and the ins-lifeguardian-qa-analyst skill.

Write detailed test cases for Group <GROUP NUMBER> only.

Before writing:
- Re-read the latest confirmed requirement decisions and reviewer feedback.
- Check related QA Second Brain cases and the approved-case ledger for duplicates.
- Read the detailed test-case style, quality gate, and SMAR-2633 approved pattern.
- Preserve approved IDs and use the next unused sequence for additions.

Output requirements:
- Use the standard UI/API/regression matrix for the group.
- Every UI/API title is plain text beginning with "Verify ".
- The first case contains the complete executable navigation and workflow path.
- Later cases remain independently reproducible but avoid unnecessary repeated navigation.
- Group Expected Result and Expected Integration by numbered step.
- Include exact values/messages/statuses, persistence, no false save, duplicate prevention, and no unintended integration where relevant.
- Put unresolved outcomes under Deferred Scenarios instead of inventing expected behaviour.
- Do not include another group and stop after Group <GROUP NUMBER> for review.
```
