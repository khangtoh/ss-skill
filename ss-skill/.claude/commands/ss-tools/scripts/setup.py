#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    config_path = skill_dir / "config.json"

    raw_path = sys.argv[1] if len(sys.argv) > 1 else input("Screenshot folder path: ").strip()
    if not raw_path:
        raise SystemExit("No folder path provided.")

    root = Path(raw_path).expanduser()
    if not root.exists():
        raise SystemExit(f"Path does not exist: {root}")
    if not root.is_dir():
        raise SystemExit(f"Path is not a directory: {root}")

    resolved_root = root.resolve()
    config_path.write_text(json.dumps({"root": str(resolved_root)}, indent=2) + "\n", encoding="utf-8")
    print(f"Saved screenshot folder: {resolved_root}")
    print(f"Config file: {config_path}")


if __name__ == "__main__":
    main()
