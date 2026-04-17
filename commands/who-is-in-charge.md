Tag the current Claude Code session with a random handle (emoji + name) drawn from `~/.claude/who-is-in-charge.json`, so the user can tell different chats/ideas apart at a glance.

**Steps:**

1. Run `python ~/.claude/scripts/who_is_in_charge.py` (use `python3` if `python` is unavailable). The script prints the full target session title to stdout and does not mutate any files.
2. Reply to the user with a single copy-pasteable line in the form: `` Run: `/rename <script output>` `` — they paste it into the Claude Code prompt to apply the rename live.
3. On script failure (non-zero exit), print stderr and stop. Do not retry.

**Notes:**

- Claude Code's built-in `/rename` is the only reliable way to update the live terminal title — writing the session JSON directly does not refresh the in-memory title until the CLI restarts. The script therefore only *computes* the target name and leaves the actual write to `/rename`.
- If the current title already starts with a known handle prefix (`<emoji> <name> - `), that prefix is stripped before the new one is prepended — so repeated runs swap the handle, they do not stack.
- To add more handles, edit `~/.claude/who-is-in-charge.json` — a JSON array of `{ "emoji": "…", "name": "…" }` objects.
