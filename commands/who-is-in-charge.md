Tag the current Claude Code session with a random handle (emoji + name) drawn from `~/.claude/who-is-in-charge.json`, so the user can tell different chats/ideas apart at a glance.

**Steps:**

1. Run `python ~/.claude/scripts/who_is_in_charge.py` (use `python3` if `python` is unavailable).
2. On success the script prints the new session title to stdout. Report it to the user verbatim, e.g. `Renamed to: 🤠 The Kid - <previous title>`.
3. On failure (non-zero exit), print stderr and stop. Do not retry.

**Notes:**

- The script mutates `~/.claude/sessions/<pid>.json` directly. The rendered session title in the terminal may not refresh until the next CLI re-read; confirm by running `/status` or starting a new prompt.
- If the current title already starts with a known handle prefix (`<emoji> <name> - `), that prefix is stripped before the new one is prepended — so repeated runs swap the handle, they do not stack.
- To add more handles, edit `~/.claude/who-is-in-charge.json` — a JSON array of `{ "emoji": "…", "name": "…" }` objects.
