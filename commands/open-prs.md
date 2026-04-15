List all open pull requests in the current repository that were not created by you, from the last 3 weeks, ordered oldest first, with line change stats.

**Steps:**

1. Get the current GitHub username by running `gh api user --jq .login`.
   - If `gh` is not available or the command fails, stop and tell the user to install/authenticate the GitHub CLI.

2. Calculate the date 3 weeks ago from today in `YYYY-MM-DD` format.

3. Run `gh pr list --state open --json number,title,url,createdAt,headRefName,baseRefName,author --limit 100` to get all open PRs.

4. Filter the results:
   - Exclude PRs where the author login matches your username from step 1.
   - Exclude PRs created before the date from step 2.

5. Sort the remaining PRs by `createdAt` ascending (oldest first).

6. For each PR, run `gh pr diff <number> --patch` and count the total lines added (`+` lines) and removed (`-` lines) from the diff. Ignore diff headers and metadata lines — only count content lines starting with `+` or `-` (excluding `+++` and `---` file headers).

7. Present the results as a Markdown table:

   | PR | Date | Source | Target | Author | Added | Removed |
   |---|---|---|---|---|---|---|
   | [#<number> <title>](<url>) | YYYY-MM-DD | `<headRefName>` | `<baseRefName>` | @<author> | +N | -N |

   - Date should be just the date portion of `createdAt`, not the full timestamp.
   - If there are no matching PRs, say so and stop.

8. After the table, show a summary line:
   > **N open PRs by others in the last 3 weeks — +X / -Y lines total**
