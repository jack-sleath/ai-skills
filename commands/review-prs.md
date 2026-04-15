Review your open pull requests in the current repository with fresh eyes, report issues grouped by severity, and offer to fix them.

**Steps:**

1. Run `gh pr list --state open --author @me --json number,title,headRefName,baseRefName --limit 50` to get your open PRs for this repo.
   - If there are no open PRs, tell the user and stop.
   - If `gh` is not available or the command fails, stop and tell the user to install/authenticate the GitHub CLI.

2. Present the list as a numbered table showing `#`, title, and branch name so the user can see what will be reviewed. Then proceed directly — no selection prompt needed.

3. For each PR, one at a time:
   a. Run `gh pr diff <number>` to get the full diff.
   b. Run `gh pr view <number> --json body,comments,reviews --jq '{body: .body, comments: [.comments[].body], reviews: [.reviews[].body]}'` to get the PR description and any existing review comments.
   c. Review the diff thoroughly, adopting the mindset of a senior developer seeing this code for the first time. Focus on:
      - **Bugs** — logic errors, off-by-ones, null/undefined access, race conditions, incorrect comparisons
      - **Security** — injection, auth bypass, secret exposure, unsafe deserialization
      - **Data loss** — destructive operations without guards, missing transactions, silent failures that swallow data
      - **Error handling** — uncaught exceptions, swallowed errors, misleading error messages
      - **Performance** — N+1 queries, unbounded loops, missing pagination, unnecessary allocations
      - **Correctness** — does the code actually do what the PR title/description claims?
      - **Edge cases** — empty inputs, boundary values, concurrent access, large payloads
   d. For each issue found, record: the file and line(s), a short description, a severity label, and a concrete suggestion for fixing it.

4. After reviewing all selected PRs, consolidate every issue into a single report grouped by severity in this order:

   ### Critical
   Issues that will cause bugs, data loss, or security vulnerabilities in production.

   ### Warning
   Issues that are likely to cause problems — poor error handling, performance traps, incorrect edge-case behaviour.

   ### Suggestion
   Improvements that would make the code cleaner, more maintainable, or more idiomatic, but are not functionally wrong.

   Within each severity group, list issues ordered by PR number. Each issue should look like:

   **PR #<number>** — `<file>:<line(s)>`
   <Description of the issue>
   *Fix:* <Concrete suggestion>

   If a PR has no issues, note it as clean:
   > **PR #<number>** — No issues found.

   At the end of the report, show a summary line:
   > **Total: X critical, Y warnings, Z suggestions across N PRs**

5. If there are any critical or warning issues, ask the user:
   > Want me to check out the branch and fix these? I'll start with the critical issues.
   > 1. Yes — fix critical issues only
   > 2. Yes — fix critical and warnings
   > 3. Yes — fix everything
   > 4. No — I'll handle it myself

   Wait for the answer.

   If the user chooses to fix:
   a. Group the selected issues by PR (so you switch branches once per PR, not per issue).
   b. For each PR with issues to fix:
      - Run `git stash` if there are uncommitted changes.
      - Run `gh pr checkout <number>` to check out the PR branch.
      - Fix each issue in that PR, one file at a time.
      - After all fixes for this PR, run `/commit` to create a commit with the fixes.
      - Push the changes: `git push`.
      - Move to the next PR.
   c. After all PRs are fixed, check out the original branch again.
   d. Run `git stash pop` if changes were stashed in step (b).
   e. Summarise what was fixed and in which PRs.

   If the user says no, just end.

**Rules:**

- Never approve or merge a PR — only review and optionally push fix commits.
- Never force-push.
- If a PR diff is extremely large (> 5000 lines), warn the user and ask whether to review it or skip it.
- Be genuinely critical. The whole point is catching things the author missed. Do not pad the report with praise or filler.
- If you are unsure whether something is a bug or intentional, label it as a **Warning** with a note explaining the ambiguity rather than silently skipping it.
- When fixing issues, make minimal targeted changes — do not refactor surrounding code.
