#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat <<'EOF'
Usage:
  ./install.sh [claude|codex|both] [--force]

Examples:
  ./install.sh
  ./install.sh codex
  ./install.sh claude --force
  ./install.sh both

If no target is provided, the installer will prompt.
EOF
}

copy_path() {
  local src="$1"
  local dest="$2"
  local force="$3"

  if [[ -e "$dest" ]]; then
    if [[ "$force" != "true" ]]; then
      printf 'Refusing to overwrite existing path without --force: %s\n' "$dest" >&2
      exit 1
    fi
    rm -rf "$dest"
  fi

  mkdir -p "$(dirname "$dest")"
  cp -R "$src" "$dest"
}

install_codex() {
  copy_path "$ROOT_DIR/.codex/skills/ss" "$HOME/.codex/skills/ss" "$FORCE"
  printf 'Installed Codex skill to %s\n' "$HOME/.codex/skills/ss"
}

install_claude() {
  copy_path "$ROOT_DIR/.claude/commands/ss.md" "$HOME/.claude/commands/ss.md" "$FORCE"
  copy_path "$ROOT_DIR/.claude/commands/ss-tools" "$HOME/.claude/commands/ss-tools" "$FORCE"
  printf 'Installed Claude command to %s\n' "$HOME/.claude/commands/ss.md"
  printf 'Installed Claude helper files to %s\n' "$HOME/.claude/commands/ss-tools"
}

prompt_target() {
  printf 'Select install target:\n'
  printf '  1. codex\n'
  printf '  2. claude\n'
  printf '  3. both\n'
  read -r -p 'Choice [1-3]: ' choice
  case "$choice" in
    1) TARGET="codex" ;;
    2) TARGET="claude" ;;
    3) TARGET="both" ;;
    *) printf 'Invalid choice: %s\n' "$choice" >&2; exit 1 ;;
  esac
}

TARGET=""
FORCE="false"

for arg in "$@"; do
  case "$arg" in
    codex|claude|both)
      if [[ -n "$TARGET" ]]; then
        printf 'Only one target may be specified.\n' >&2
        exit 1
      fi
      TARGET="$arg"
      ;;
    --force)
      FORCE="true"
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'Unknown argument: %s\n\n' "$arg" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ -z "$TARGET" ]]; then
  prompt_target
fi

case "$TARGET" in
  codex)
    install_codex
    ;;
  claude)
    install_claude
    ;;
  both)
    install_codex
    install_claude
    ;;
esac
