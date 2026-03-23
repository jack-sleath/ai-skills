Review the current changes and create a local git commit with a well-crafted message.

**Steps:**

1. Run `git status` to see what files are staged/unstaged.
2. Run `git diff HEAD` to understand what has actually changed.
3. Check whether the diff touches any files in `commands/`:
   - If a skill file was **added or removed**, verify `README.md` has been updated to reflect the change. If not, update it before proceeding.
   - If a skill file was **added, removed, or changed in a way that affects how skills delegate to or depend on each other**, verify `SKILL-GRAPH.md` has been updated to reflect the change. If not, update it before proceeding.
4. Scan the diff for encoding corruption (mojibake sequences like `Ã¢â‚¬"`, `Ã¢â‚¬â„¢`, `ÃƒÂ©`, etc.). If any are found:
   - Draft a tentative commit message describing what the change *would* commit (e.g. "Fix encoding in commit.md") so the user knows what to expect after remediation.
   - If the corrupted file is in `commands/`, also note whether `README.md` and `SKILL-GRAPH.md` will need to be verified once encoding is fixed.
   - **Block the commit and ask the user to fix the encoding before proceeding** — do not commit corrupted content.
5. Analyse the changes and draft a commit message:
   - First line: short imperative summary (max 72 chars), e.g. "Add retry logic to API client"
   - If the change warrants it, add a blank line then a short body (2-4 lines) explaining *why*, not just what
   - Notable issues discovered during the commit process (e.g. files skipped, manual steps needed) belong in the commit body, not only in CLI output
   - Do not include filler like "various improvements" or "minor changes" — be specific
6. Stage all modified tracked files with `git add -u`, unless the user specified particular files.
7. Commit locally using the drafted message. Pass the message via heredoc to preserve formatting:
   ```
   git commit -m "$(cat <<'EOF'
   <subject line>

   <optional body>
   EOF
   )"
   ```
8. Confirm the commit succeeded with `git log -1 --oneline`.

**Rules:**
- Never push to the remote.
- Never use `--no-verify`.
- Never commit files that look like secrets (`.env`, credential files, private keys).
- Never commit files containing encoding corruption — block and ask the user to fix first. When blocking, always provide a tentative commit message so the user knows what will be committed after remediation.
- When blocking a commit on a file in `commands/`, remind the user that `README.md` and `SKILL-GRAPH.md` may also need to be verified once the issue is resolved.
- If nothing is staged and nothing is modified, report that there is nothing to commit.
- Output only what is necessary: skip meta-commentary about eval fixtures or execution context.
- When reporting a blocked commit, state the issue and tentative message once — do not restate mojibake examples in the fix instructions. Keep the remediation note to one sentence.