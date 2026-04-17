Tag the current Claude Code session with a random handle (emoji + name) drawn from `~/.claude/who-is-in-charge.json`, so the user can tell different chats/ideas apart at a glance.

**Steps:**

1. Run this single pipeline (use `python3` if `python` is unavailable):

   ```bash
   VALUE=$(python ~/.claude/scripts/who_is_in_charge.py) && \
     printf '/rename %s' "$VALUE" | python ~/.claude/scripts/copy_to_clipboard.py && \
     echo "/rename $VALUE"
   ```

   The first script computes the target session title. The `printf | copy_to_clipboard.py` step puts the full `/rename <title>` line on the OS clipboard (using stdin — avoids git-bash's path conversion of the leading `/`). The final `echo` lets you see what was copied.

2. Tell the user their new session title and that it's on the clipboard, ready to paste. Example: ``Copied `/rename 🤓 Nerd - <previous title>` to your clipboard — paste (Ctrl+V) and press Enter.``

3. On any non-zero exit from the pipeline, print stderr and stop. Do not retry.

**Notes:**

- Claude Code's built-in `/rename` is the only reliable way to update the live terminal title — writing the session JSON directly does not refresh the in-memory title until the CLI restarts. The script therefore only *computes* the target name; the user applies it by pasting the clipboard contents into the prompt.
- The copied line also lands in the Win+V clipboard history panel if Windows clipboard history is enabled (Settings → System → Clipboard).
- If the current title already starts with a known handle prefix (`<emoji> <name> - `), that prefix is stripped before the new one is prepended — so repeated runs swap the handle, they do not stack.
- To add more handles, edit `~/.claude/who-is-in-charge.json` — a JSON array of `{ "emoji": "…", "name": "…" }` objects.
