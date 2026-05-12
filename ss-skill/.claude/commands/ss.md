---
allowed-tools:
  - Bash(python3 ${CLAUDE_PLUGIN_ROOT}/ss-tools/scripts/setup.py:*)
  - Bash(python3 ${CLAUDE_PLUGIN_ROOT}/ss-tools/scripts/resolve_screenshot.py:*)
  - Read
argument-hint: [index|search text]
description: Resolve a screenshot from a configured folder and inspect it
---

Use the installed screenshot helper for this command.

Workflow:

1. If `~/.claude/commands/ss-tools/config.json` does not exist, ask the user: `What folder should I use for screenshots?`
2. After the user replies, run:
   `python3 ~/.claude/commands/ss-tools/scripts/setup.py "<user-path>"`
3. Resolve the screenshot by running:
   `python3 ~/.claude/commands/ss-tools/scripts/resolve_screenshot.py --json "$ARGUMENTS"`
4. Numeric arguments are zero-based:
   - `0` = newest screenshot
   - `1` = second newest screenshot
5. If a path is returned, inspect that image file in Claude Code if the client supports local image inspection. Otherwise, return the resolved path and explain what was found.
6. If no match is found, tell the user which folder was searched and mention top candidate names when available.
