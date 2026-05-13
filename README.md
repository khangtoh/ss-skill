# ss skill

Installs a local screenshot helper for Codex and Claude Code.

The helper lets you resolve screenshots from a configured folder with:

- `ss 0` for the newest screenshot
- `ss 1` for the second newest screenshot
- `ss login` or any other text to search by filename or path

## Repository layout

- `ss-skill/install.sh`: installer script
- `ss-skill.zip`: packaged copy of the skill and Claude command files

## Installation

From the repo root:

```bash
cd ss-skill
./install.sh
```

The installer supports these targets:

```bash
./install.sh codex
./install.sh claude
./install.sh both
./install.sh codex --force
```

If you do not pass a target, the script prompts for one.

`--force` overwrites an existing installation. Without it, the installer refuses to replace existing files.

### Install locations

- Codex: `~/.codex/skills/ss`
- Claude Code command: `~/.claude/commands/ss.md`
- Claude helper files: `~/.claude/commands/ss-tools`

## Codex usage

After installing for Codex, ask for screenshots with prompts like:

```text
ss 0
ss 2
ss login
ss checkout error
```

On first use, if `~/.codex/skills/ss/config.json` does not exist, the skill asks which screenshot folder it should use. After you reply, it stores that directory and retries the original request.

You can also configure it directly:

```bash
python3 ~/.codex/skills/ss/scripts/setup.py "/absolute/path/to/screenshots"
```

Once configured, the resolver runs from:

```bash
python3 ~/.codex/skills/ss/scripts/resolve_screenshot.py --json "0"
```

## Claude Code usage

After installing for Claude Code, use the `ss` command with the same arguments:

```text
/ss 0
/ss login
```

On first use, if `~/.claude/commands/ss-tools/config.json` does not exist, the command asks for the screenshot folder and saves it with:

```bash
python3 ~/.claude/commands/ss-tools/scripts/setup.py "/absolute/path/to/screenshots"
```

## How matching works

- Numeric arguments are zero-based and sorted newest first.
- String arguments search filenames and paths case-insensitively.
- The resolver searches recursively under the configured folder.
- Matching prefers exact basename matches, then prefix matches, then substring and fuzzy matches.

Supported file types:

- `.png`
- `.jpg`
- `.jpeg`
- `.webp`
- `.gif`
- `.bmp`
- `.tif`
- `.tiff`

## Notes

- The setup path must already exist and must be a directory.
- Birth time is used for sorting when available; otherwise modification time is used.
- If no screenshot matches, the helper reports the searched folder and may include top candidates for string searches.
