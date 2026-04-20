#!/usr/bin/env python3
"""Merge a seed JSON data file into a live JSON data file, preserving user edits.

Used by install.ps1 / install.sh so that adding new entries to the repo's
`data/*.json` files flows into existing installs without clobbering any local
additions the user has made.

Merge rule: for JSON files whose top level is a non-empty array of objects
that all carry a `name` field, treat `name` as the unique key. Entries in the
seed that are not already present in the live file (by `name`) are appended;
existing live entries are kept as-is (user wins on conflict). Any other JSON
shape is left untouched.

Prints one status line on stdout so the installer can pass it through:
    Copied (Data): <file>           live did not exist → plain copy
    Unchanged (Data): <file>        live already had every seed entry
    Merged (Data, +N): <file>       N seed entries appended
    Skipped (Data, <reason>): <file>  shape not mergeable / unparseable

Exit 0 on success (including Skipped); exit 1 only on argv/IO errors that
the installer should surface.
"""
import json
import shutil
import sys
from pathlib import Path


def is_array_of_named_objects(x) -> bool:
    if not isinstance(x, list) or not x:
        return False
    return all(isinstance(item, dict) and "name" in item for item in x)


def format_compact_array(items) -> str:
    """Render a list of JSON objects one-per-line inside a top-level array,
    matching the hand-written style of the repo's seed files."""
    lines = ["["]
    for i, item in enumerate(items):
        obj = json.dumps(item, ensure_ascii=False)
        sep = "," if i < len(items) - 1 else ""
        lines.append(f"  {obj}{sep}")
    lines.append("]")
    return "\n".join(lines) + "\n"


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: merge_data_json.py <seed> <live>", file=sys.stderr)
        return 1

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

    seed_path = Path(sys.argv[1])
    live_path = Path(sys.argv[2])
    name = seed_path.name

    if not seed_path.exists():
        print(f"ERROR: seed file {seed_path} not found", file=sys.stderr)
        return 1

    if not live_path.exists():
        live_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(seed_path, live_path)
        print(f"Copied (Data): {name}")
        return 0

    try:
        seed = json.loads(seed_path.read_text(encoding="utf-8"))
        live = json.loads(live_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"Skipped (Data, unparseable): {name} ({e})")
        return 0

    if not is_array_of_named_objects(seed) or not is_array_of_named_objects(live):
        print(f"Skipped (Data, unmergeable shape): {name}")
        return 0

    live_names = {item["name"] for item in live}
    added = [item for item in seed if item["name"] not in live_names]
    if not added:
        print(f"Unchanged (Data): {name}")
        return 0

    merged = list(live) + added
    live_path.write_text(format_compact_array(merged), encoding="utf-8")
    print(f"Merged (Data, +{len(added)}): {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
