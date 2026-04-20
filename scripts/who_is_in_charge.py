#!/usr/bin/env python3
"""Pick a random handle from ~/.claude/who-is-in-charge.json and print the full
target session title, so the caller can feed it to Claude Code's built-in
`/rename` command.

Format: `<emoji> <name> - <cwd basename>`. The folder basename is always used
as the suffix — repeated runs swap the handle but keep the same suffix, so the
session title stays stable and tied to the project directory.

Prints only the target title to stdout. Does not mutate any files — use
`/rename <output>` to apply, which updates both the session JSON and the live
terminal title.
"""
import json
import os
import random
import sys
from pathlib import Path


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

    home = Path.home()
    handles_file = home / ".claude" / "who-is-in-charge.json"

    if not handles_file.exists():
        print(f"ERROR: {handles_file} not found", file=sys.stderr)
        return 1

    try:
        handles = json.loads(handles_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERROR: {handles_file} is not valid JSON: {e}", file=sys.stderr)
        return 1

    if not isinstance(handles, list) or not handles:
        print(f"ERROR: {handles_file} must be a non-empty array", file=sys.stderr)
        return 1

    cwd = Path(os.getcwd()).resolve()
    suffix = cwd.name or str(cwd)  # fall back to full path at a drive root like "C:\"

    pick = random.choice(handles)
    print(f"{pick['emoji']} {pick['name']} - {suffix}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
