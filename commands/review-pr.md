Review a single open pull request selected from the list produced by `/open-prs`, output the review in the terminal, and optionally post it as a comment on the PR.

**Steps:**

1. Run `/open-prs` to display the table of open PRs by others from the last 3 weeks.
   - If there are no matching PRs, stop.

2. Ask the user:
   > Which PR should I review? (enter the PR number)

   Wait for the answer.

3. Fetch the PR details:
   a. Run `gh pr diff <number>` to get the full diff.
   b. Run `gh pr view <number> --json title,body,comments,reviews --jq '{title: .title, body: .body, comments: [.comments[].body], reviews: [.reviews[].body]}'` to get the PR description and any existing review comments.

4. Review the diff thoroughly, adopting the mindset of a senior developer seeing this code for the first time. Focus on:
   - **Bugs** — logic errors, off-by-ones, null/undefined access, race conditions, incorrect comparisons
   - **Security** — injection, auth bypass, secret exposure, unsafe deserialization
   - **Data loss** — destructive operations without guards, missing transactions, silent failures that swallow data
   - **Error handling** — uncaught exceptions, swallowed errors, misleading error messages
   - **Performance** — N+1 queries, unbounded loops, missing pagination, unnecessary allocations
   - **Correctness** — does the code actually do what the PR title/description claims?
   - **Edge cases** — empty inputs, boundary values, concurrent access, large payloads

5. Output the review in the terminal using this format:

   ## Review — PR #<number>: <title>

   ### Critical
   Issues that will cause bugs, data loss, or security vulnerabilities in production.

   **`<file>:<line(s)>`**
   <Description of the issue>
   *Fix:* <Concrete suggestion>

   ### Warning
   Issues that are likely to cause problems — poor error handling, performance traps, incorrect edge-case behaviour.

   **`<file>:<line(s)>`**
   <Description of the issue>
   *Fix:* <Concrete suggestion>

   ### Suggestion
   Improvements that would make the code cleaner, more maintainable, or more idiomatic, but are not functionally wrong.

   **`<file>:<line(s)>`**
   <Description of the issue>
   *Fix:* <Concrete suggestion>

   ---
   **Summary: X critical, Y warnings, Z suggestions**

   - Omit any severity section that has no issues (don't show empty headings).
   - If the PR is clean, just say: **No issues found.**
   - Be genuinely critical — the point is catching things the author missed. No filler or praise.
   - If unsure whether something is a bug or intentional, include it as a **Warning** with a note explaining the ambiguity.

6. After displaying the review, ask the user:
   > Want me to post this review as a comment on the PR?
   > 1. Yes — post it
   > 2. No

   Wait for the answer.

   If yes:
   - Post the review as a PR comment using `gh pr comment <number> --body "<review>"`. Use a heredoc to pass the body safely.
   - Confirm the comment was posted and show the PR URL.

   If no, just end.

**Rules:**

- Never approve or merge the PR — only review and optionally comment.
- Do not modify any files or switch branches — this is a read-only review.
- If the PR diff is extremely large (> 5000 lines), warn the user and ask whether to proceed or skip.
