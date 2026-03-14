Review the current changes and create a local git commit with a well-crafted message.

**Steps:**

1. Run `git status` to see what files are staged/unstaged.
2. Run `git diff HEAD` to understand what has actually changed.
3. Analyse the changes and draft a commit message:
   - First line: short imperative summary (max 72 chars), e.g. "Add retry logic to API client"
   - If the change warrants it, add a blank line then a short body (2–4 lines) explaining *why*, not just what
   - Do not include filler like "various improvements" or "minor changes" — be specific
4. Stage all modified tracked files with `git add -u`, unless the user specified particular files.
5. Commit locally using the drafted message. Pass the message via heredoc to preserve formatting:
   ```
   git commit -m "$(cat <<'EOF'
   <subject line>

   <optional body>
   EOF
   )"
   ```
6. Confirm the commit succeeded with `git log -1 --oneline`.

**Rules:**
- Never push to the remote.
- Never use `--no-verify`.
- Never commit files that look like secrets (`.env`, credential files, private keys).
- If nothing is staged and nothing is modified, report that there is nothing to commit.
