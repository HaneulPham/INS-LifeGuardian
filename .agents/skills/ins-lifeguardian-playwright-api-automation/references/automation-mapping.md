# API automation mapping

Maintain two synchronized views:

- executable JSON: `automation/api/mappings/automation-map.json`;
- Second Brain summary: `qa-knowledge/automation/api-automation-map.md`.

Allowed statuses:

- Candidate
- Automated
- Partially Automated
- Blocked
- Not Suitable
- Maintenance Required

Rules:

- One entry per manual test-case ID.
- `Automated` requires an existing spec file, exact test title, endpoint/method, validation success, and an evidence-backed last result when execution was possible.
- `Partially Automated` must state the manual remainder.
- `Blocked` must name the missing contract, access, data, environment, or instrumentation.
- `Not Suitable` must explain why safe deterministic automation is inappropriate.
- `Maintenance Required` preserves the prior implementation but indicates it is not currently reliable.
- Never change the manual test case's approval/status merely because automation exists.
- Update mapping only after review or execution evidence; never infer a pass.
