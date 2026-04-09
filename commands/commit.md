Review the current changes and create a local git commit with a well-crafted message.

**Steps:**

1. Run `git status` and `git diff HEAD` to understand what has changed.
2. If nothing is staged or modified, report "nothing to commit" and stop.
3. Scan the diff for encoding corruption (mojibake: `Ã¢â‚¬"`, `Ã¢â‚¬â„¢`, `ÃƒÂ©`, etc.). If found: state the tentative commit message, block the commit, ask the user to fix it.
4. Scan the diff for secrets: API keys, tokens, passwords, private keys, `.env` files, or patterns like `KEY=`, `TOKEN=`, `SECRET=` assigned to long hex/base64 strings. If found: block the commit and name the file and pattern.
5. Draft the commit message:
   - Subject: imperative, ≤72 chars, specific (not "various improvements")
   - Body (if warranted): 2–4 lines explaining *why*, naming the component. Include any notable issues (skipped files, manual steps needed).
6. Stage with `git add -u` (or user-specified files), then commit via heredoc:
   ```
   git commit -m "$(cat <<'EOF'
   <subject>

   <optional body>
   EOF
   )"
   ```
7. Confirm with `git log -1 --oneline`.

**Rules:**
- Never push, never `--no-verify`, never commit secrets or encoding corruption.
- Output only what's necessary — no closing paragraphs restating tree state, no meta-commentary.
- When blocking, state the issue and tentative message once.
