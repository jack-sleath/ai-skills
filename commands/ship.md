Continuously implement milestones one at a time, raising a PR to the main branch after each one before moving on to the next.

**Steps to follow for each milestone:**

1. Read the milestones file and identify the lowest-numbered incomplete milestone. If all milestones are complete, stop and report that the project is fully shipped.
2. Determine the main branch name — check for `main` or `master` (use `git remote show origin` or inspect `git branch -r` if unsure).
3. Check out the main branch and pull the latest changes, then create a new branch named `milestone-N` from it.
4. Follow all steps in the `/milestone` command to implement, test, commit, and push the milestone — including auto-discovering and running any test or build commands before marking it complete.
5. Open a PR from `milestone-N` into the main branch:
    - First try `gh pr create` with a clear title and short body summarising what the milestone delivered.
    - If `gh` is not available or fails, fall back to constructing a compare URL from the git remote: get the remote URL with `git remote get-url origin`, convert it to an HTTPS GitHub URL if needed, and output a link in the form `https://github.com/<owner>/<repo>/compare/<main>...<milestone-N>` so the user can open the PR manually.
    - Output the PR URL (or compare URL) so the user can see it.
6. Without waiting for the PR to be merged, immediately return to step 1 and begin the next milestone.

**Rules:**

- Work one milestone at a time. Do not build ahead.
- Always branch off the latest main — do not stack milestone branches on top of each other.
- All rules from `/milestone` apply to each milestone implemented here.
- Always output a usable URL after each milestone, whether from `gh` or constructed manually.
