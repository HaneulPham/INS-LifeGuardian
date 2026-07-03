# Bug Patterns and Bug Writing Memory

Use this file to preserve bug-writing decisions and recurring bug patterns.

## Bug report format

Bug reports should use labeled sections, not a table, unless the user explicitly asks for a table:

- Title
- Summary
- Environment
- Path
- Preconditions
- Steps to Reproduce
- Actual Result
- Expected Result
- Frequency
- Severity/Priority
- Impact/Notes

## Quality rules

- Actual Result must describe observed behavior.
- Expected Result must come from a requirement, confirmed business expectation, or clearly marked QA assumption.
- Do not claim root cause without logs, API/database evidence, or developer confirmation.
- Include safety, operational, notification, integration, data, and regression impact when relevant.
