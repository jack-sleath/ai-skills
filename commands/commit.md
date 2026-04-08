Review the current changes and create a local git commit with a well-crafted message.

**Steps:**

1. Run the pre-commit scanner to check for issues:
   ```
   python ~/.claude/scripts/commit_scan.py
   ```
   - If it reports **BLOCKED**: state the tentative commit message, show the scanner output, and ask the user to fix the issues. Do not commit.
   - If it reports **Skill file changes detected**: verify `README.md` and `SKILL-GRAPH.md` are updated. If not, update them before committing.
   - If it reports **OK**: proceed.

2. Run `git diff HEAD` to understand the changes.

3. Draft the commit message:
   - Subject: imperative, ≤72 chars, specific (not "various improvements")
   - Body (if warranted): 2–4 lines explaining *why*, naming the component. Include any notable issues (skipped files, manual steps needed).

4. Stage with `git add -u` (or user-specified files), then commit via heredoc:
   ```
   git commit -m "$(cat <<'EOF'
   <subject>

   <optional body>
   EOF
   )"
   ```

5. Confirm with `git log -1 --oneline`.

**Rules:**
- Never push, never `--no-verify`, never commit secrets or encoding corruption.
- Output only what's necessary — no closing paragraphs restating tree state, no meta-commentary.
- When blocking, state the issue and tentative message once.
