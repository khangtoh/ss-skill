---
name: ss
description: Use when the user wants to pull a local screenshot into context with `ss <number>` or `ss <search text>`. `ss 0` means the newest screenshot in a configured folder, `ss 1` the second newest, and so on. `ss login` or any other string finds the best filename/path match. If the screenshot resolves successfully, attach it for visual inspection with the native local image tool.
---

# ss

Resolve a screenshot from a user-configured folder, then load the image into context.

## Setup

If `~/.codex/skills/ss/config.json` does not exist:

1. Ask the user directly: `What folder should I use for screenshots?`
2. Wait for the user's reply.
3. Run:

```bash
python3 ~/.codex/skills/ss/scripts/setup.py "<user-path>"
```

4. After setup completes, retry the original `ss <arg>` request.

The setup script stores the provided folder path in the skill config. If no argument is passed, it prompts interactively, but the preferred flow is to pass the user's path automatically.

## Use

For any `ss <arg>` request:

1. Resolve the image:

```bash
python3 ~/.codex/skills/ss/scripts/resolve_screenshot.py --json "<arg>"
```

2. Interpret the result:
- `kind: "index"` means `<arg>` was numeric and the resolver selected the zero-based image index, newest first.
- `kind: "search"` means `<arg>` was treated as a case-insensitive filename/path search.
- Sorting uses filesystem birth time when available, else modification time.

3. If a path is returned, load the image with the local image tool:
- Call `view_image` with the absolute path.
- Prefer `detail: original` when fidelity matters.

4. If no match is found, tell the user which folder was searched and, for string searches, mention the top candidate names when available.

## Notes

- The resolver searches recursively under the configured folder.
- Match quality prefers exact basename matches, then prefix matches, then substring/fuzzy matches.
- Supported file types: `.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`, `.bmp`, `.tif`, `.tiff`.
