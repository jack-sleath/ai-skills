Review the current changes and create one or more local git commits, grouping related changes together so each commit tells a single story.

**Steps:**

1. Run `git status` and `git diff HEAD` to understand what has changed. Also run `git log --oneline -5` once up-front so you can match the repo's commit-message style.
2. If nothing is staged or modified, report "nothing to commit" and stop.
3. Scan the full diff **once, before any commits** for:
   - **Encoding corruption** (mojibake: `Ã¢â‚¬"`, `Ã¢â‚¬â„¢`, `ÃƒÂ©`, etc.).
   - **Secrets**: API keys, tokens, passwords, private keys, `.env` files, or patterns like `KEY=`, `TOKEN=`, `SECRET=` assigned to long hex/base64 strings.

   If either is found: state the finding, name the file and pattern, and stop. Do not commit anything (partial commits leave the repo in a half-done state that's painful to unwind).
4. **Group the changes into logical batches.** Each batch becomes one commit. A batch is a set of files that share a single purpose — if you'd write "and" in the subject line to cover the whole batch, split it. Common separators:
   - Unrelated features / fixes / refactors → separate batches.
   - **Generated or build artefacts** (`dist/`, `build/`, `*.min.*`, bundled `.js`/`.css`, compiled binaries, regenerated lockfiles) → their own batch, committed **after** the source change that produced them, so the history reads "change X" then "rebuild dist for X".
   - Formatting / whitespace-only changes → separate from logic changes.
   - Standalone doc or comment fixes → separate, unless they document a code change in the same batch.
   - Tests + the code they cover → same batch.
   - Config / dependency bumps unrelated to other work → their own batch.

   List the planned batches to yourself (file list + one-line purpose each) before you start committing. If there's only one logical group, that's fine — one commit.
5. **Commit each batch in order.** For each batch:
   1. Stage only that batch's files explicitly by path (`git add <file1> <file2> …`). Never use `git add -A` / `git add .` / `git add -u` when batching — they'll sweep in files from other batches. Include new files (currently untracked) in whichever batch they belong to.
   2. Draft the message:
      - Subject: imperative, ≤72 chars, specific (not "various improvements"). Match the style from `git log --oneline -5`.
      - Body (if warranted): 2–4 lines explaining *why*, naming the component. Include notable issues (skipped files, manual steps needed).
   3. Commit via heredoc:
      ```
      git commit -m "$(cat <<'EOF'
      <subject>

      <optional body>
      EOF
      )"
      ```
   4. Run `git status` to confirm the batch landed and see what's left.
6. After the last batch, run `git log --oneline -<N>` (where N = number of commits you just made) to show the user the resulting history.

**Rules:**
- Never push, never `--no-verify`, never commit secrets or encoding corruption.
- Never amend a previous commit in this loop — if a pre-commit hook fails, fix the issue and create a **new** commit for that batch.
- If staging a batch leaves the working tree empty before you've committed all batches, something grouped wrong — stop and re-check.
- One batch is fine. Don't split just to split — the goal is that each commit has a coherent subject, not a commit count.
- Output only what's necessary — no closing paragraphs restating tree state, no meta-commentary. A short per-batch line ("batch 2/3: dist rebuild — committed as abc1234") is enough.
- When blocking (step 3), state the issue once and stop; do not partially commit.
