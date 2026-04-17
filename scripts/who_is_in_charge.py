#!/usr/bin/env python3
"""Pick a random handle from ~/.claude/who-is-in-charge.json and print the full
target session title, so the caller can feed it to Claude Code's built-in
`/rename` command.

Locates the current session by matching cwd against ~/.claude/sessions/*.json,
picking the most recently modified match, and strips any existing handle prefix
from the current name so repeated runs swap handles instead of stacking.

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
    sessions_dir = home / ".claude" / "sessions"
    handles_file = home / ".claude" / "who-is-in-charge.json"
    cwd = Path(os.getcwd()).resolve()

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

    current = ""
    if sessions_dir.exists():
        candidates = []
        for f in sessions_dir.glob("*.json"):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            session_cwd_raw = data.get("cwd")
            if not session_cwd_raw:
                continue
            try:
                session_cwd = Path(session_cwd_raw).resolve()
            except (OSError, ValueError):
                continue
            if session_cwd == cwd:
                candidates.append((f.stat().st_mtime, data))
        if candidates:
            candidates.sort(reverse=True)
            current = candidates[0][1].get("name", "") or ""

    original = current
    for h in handles:
        emoji = h.get("emoji", "")
        name = h.get("name", "")
        prefix = f"{emoji} {name} - "
        if current.startswith(prefix):
            original = current[len(prefix):]
            break

    pick = random.choice(handles)
    new_name = f"{pick['emoji']} {pick['name']} - {original}" if original else f"{pick['emoji']} {pick['name']}"
    print(new_name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
