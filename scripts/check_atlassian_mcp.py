#!/usr/bin/env python3
"""Run a non-sensitive initialization and Jira health check against Atlassian MCP."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / ".codex/config.toml"
REQUIRED_CREDENTIALS = ("ATLASSIAN_EMAIL", "ATLASSIAN_API_TOKEN")


def fail(message: str) -> int:
    print(f"FAIL: {message}")
    return 1


def main() -> int:
    config_text = CONFIG_PATH.read_text(encoding="utf-8")
    package_match = re.search(r'"(mcp-atlassian@\d+\.\d+\.\d+)"', config_text)
    base_url_match = re.search(
        r'^ATLASSIAN_BASE_URL\s*=\s*"([^"]+)"\s*$', config_text, re.MULTILINE
    )
    if package_match is None or base_url_match is None:
        return fail("invalid or unpinned .codex/config.toml Atlassian MCP settings")

    missing = [name for name in REQUIRED_CREDENTIALS if not os.environ.get(name)]
    if missing:
        return fail("missing environment variables: " + ", ".join(missing))

    environment = os.environ.copy()
    environment["ATLASSIAN_BASE_URL"] = base_url_match.group(1)

    messages = [
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "ins-lifeguardian-health-check", "version": "1.0"},
            },
        },
        {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "get_jira_current_user", "arguments": {}},
        },
    ]

    try:
        result = subprocess.run(
            [
                "npx",
                "--cache",
                str(PROJECT_ROOT / ".cache/npm-mcp"),
                "-y",
                package_match.group(1),
            ],
            cwd=PROJECT_ROOT,
            env=environment,
            input="".join(json.dumps(message) + "\n" for message in messages),
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return fail(f"Atlassian MCP did not initialize: {type(error).__name__}")

    responses: dict[int, dict[str, object]] = {}
    for line in result.stdout.splitlines():
        try:
            response = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(response, dict) and isinstance(response.get("id"), int):
            responses[response["id"]] = response

    if "result" not in responses.get(1, {}):
        return fail("Atlassian MCP initialization failed")
    tools = responses.get(2, {}).get("result", {}).get("tools", [])
    if not isinstance(tools, list) or not tools:
        return fail("Atlassian MCP returned no tools")
    health_result = responses.get(3, {}).get("result", {})
    if not isinstance(health_result, dict) or health_result.get("isError", False):
        return fail("Jira authentication health check failed")

    print(f"PASS: Atlassian MCP initialized; tools={len(tools)}; Jira authentication verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
