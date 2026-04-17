#!/usr/bin/env python3
"""Prepend a random handle from ~/.claude/who-is-in-charge.json to the current
Claude Code session's title, so the user can tell different chats apart at a glance.

Locates the session by matching the current working directory against the `cwd`
field in ~/.claude/sessions/*.json, picking the most recently modified match.
Writes the new `name` back to the same JSON file.

Idempotent: if the current title already starts with a handle from the list,
that prefix is stripped before the new one is prepended, so re-running the
command swaps the handle instead of stacking them.
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

    if not sessions_dir.exists():
        print(f"ERROR: {sessions_dir} not found", file=sys.stderr)
        return 1

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
            candidates.append((f.stat().st_mtime, f, data))

    if not candidates:
        print(f"ERROR: no session file matching cwd {cwd}", file=sys.stderr)
        return 1

    candidates.sort(reverse=True)
    _, session_file, data = candidates[0]
    current = data.get("name", "") or ""

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

    data["name"] = new_name
    session_file.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    print(new_name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
