# Atlassian MCP Configuration

INS LifeGuardian pins the project-scoped Atlassian MCP server to `mcp-atlassian@2.0.1` in `.codex/config.toml`.

This version was selected because it completed an MCP initialize handshake, exposed its tool list, and passed a read-only Jira authentication check. Published versions `2.0.2` and `2.1.0` were not selected because startup testing on 2026-07-20 failed on their unresolved runtime `jsdom` import.

## Authentication

Codex must receive these credentials from its environment:

- `ATLASSIAN_EMAIL`
- `ATLASSIAN_API_TOKEN`

The non-secret `ATLASSIAN_BASE_URL` is configured in `.codex/config.toml`.

Never store an Atlassian API token in Git, `.codex/config.toml`, documentation, shell history, or QA Second Brain files. Configure the variables in the environment that launches Codex and restart Codex after changing them. Revoke and rotate a token immediately if it has been stored or displayed in plaintext.

## Connection Health Check

From the repository root, run:

```bash
python3 scripts/check_atlassian_mcp.py
```

The script performs only:

1. MCP initialization.
2. Tool-list discovery.
3. A read-only `get_jira_current_user` authentication call.

It reports status and tool count without printing credential values or returned user details.

## Unavailable Jira or Confluence

The MCP server is configured with `required = false` so repository review, validator maintenance, and supplied-evidence QA work remain available offline. Jira remains the highest-priority source when a ticket key is present.

When Jira or Confluence is unavailable during QA analysis:

- Report the unavailable source under **Could Not Verify**.
- Do not present QA Second Brain content, repository evidence, or model memory as a substitute for inaccessible current Jira/Confluence evidence.
- Do not convert missing evidence into a Confirmed result.
- Record any necessary inference as a clearly labelled **QA Assumption** or **Open Question**.
- Stop an approval or automatic Second Brain update when the missing private evidence could change the intended behavior.

Restart Codex after changing `.codex/config.toml`, then run the health check again.
