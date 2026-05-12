#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff"}


@dataclass
class Candidate:
    path: Path
    relative_path: str
    basename: str
    stem: str
    added_ts: float


def default_config_path() -> Path:
    return Path(__file__).resolve().parent.parent / "config.json"


def load_root(config_path: Path) -> Path:
    if not config_path.exists():
        raise SystemExit(f"Missing config file: {config_path}")
    data = json.loads(config_path.read_text(encoding="utf-8"))
    root = Path(data["root"]).expanduser()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Configured screenshot folder is invalid: {root}")
    return root.resolve()


def image_paths(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
            yield path


def added_timestamp(path: Path) -> float:
    stat = path.stat()
    birth = getattr(stat, "st_birthtime", None)
    if birth is not None and birth > 0:
        return float(birth)
    return float(stat.st_mtime)


def build_candidates(root: Path) -> list[Candidate]:
    items = []
    for path in image_paths(root):
        items.append(
            Candidate(
                path=path.resolve(),
                relative_path=str(path.resolve().relative_to(root)),
                basename=path.name.lower(),
                stem=path.stem.lower(),
                added_ts=added_timestamp(path),
            )
        )
    return items


def pick_by_index(candidates: list[Candidate], raw: str) -> Candidate:
    index = int(raw)
    if index < 0:
        raise SystemExit("Numeric lookup must be >= 0.")
    ordered = sorted(candidates, key=lambda item: (item.added_ts, item.relative_path), reverse=True)
    if index >= len(ordered):
        raise SystemExit(f"Requested screenshot #{index}, but only {len(ordered)} images were found.")
    return ordered[index]


def score_candidate(query: str, item: Candidate) -> tuple[float, float]:
    q = query.lower().strip()
    rel = item.relative_path.lower()
    stem = item.stem
    base = item.basename

    score = 0.0
    if q == stem:
        score += 1000
    if q == base:
        score += 950
    if stem.startswith(q):
        score += 700
    if base.startswith(q):
        score += 650
    if q in stem:
        score += 500
    if q in rel:
        score += 350

    score += difflib.SequenceMatcher(None, q, stem).ratio() * 100
    score += difflib.SequenceMatcher(None, q, rel).ratio() * 50
    return score, item.added_ts


def pick_by_search(candidates: list[Candidate], raw: str) -> tuple[Candidate, list[Candidate]]:
    ranked = sorted(candidates, key=lambda item: score_candidate(raw, item), reverse=True)
    if not ranked:
        raise SystemExit("No screenshots were found in the configured folder.")
    return ranked[0], ranked[:5]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Numeric index or search text.")
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument(
        "--config",
        default=None,
        help="Optional config path with the screenshot root.",
    )
    args = parser.parse_args()

    config_path = Path(args.config).expanduser() if args.config else default_config_path()
    root = load_root(config_path)
    candidates = build_candidates(root)
    if not candidates:
        raise SystemExit(f"No supported images were found in {root}")

    query = args.query.strip()
    if query.isdigit():
        selected = pick_by_index(candidates, query)
        payload = {
            "kind": "index",
            "query": query,
            "root": str(root),
            "path": str(selected.path),
            "relative_path": selected.relative_path,
        }
    else:
        selected, ranked = pick_by_search(candidates, query)
        payload = {
            "kind": "search",
            "query": query,
            "root": str(root),
            "path": str(selected.path),
            "relative_path": selected.relative_path,
            "candidates": [item.relative_path for item in ranked],
        }

    if args.as_json:
        print(json.dumps(payload, indent=2))
    else:
        print(payload["path"])


if __name__ == "__main__":
    main()
