Create a staging branch off a target base branch, then merge the current feature branch into it.

Arguments: $ARGUMENTS
- Optional: the target base branch (e.g. `UAT/main`, `staging/main`). If not provided, prompt the user to select one interactively.

**Steps:**

1. Run `git branch --show-current` to get the current branch name.
2. Extract the ticket identifier from the current branch name — assume the branch name is `<prefix>/<IDENTIFIER>` and the identifier is everything after the first `/`. If the branch doesn't follow this pattern, stop and tell the user.
3. If no base branch was provided in $ARGUMENTS:
   - Fetch the latest from origin: `git fetch origin`.
   - List all remote branches: `git branch -r | sed 's|origin/||' | sed 's|^[[:space:]]*||' | grep -v 'HEAD'`
   - Check if `fzf` is available: `command -v fzf`
   - If `fzf` is available, pipe the branch list into it for interactive fuzzy filtering:
     `git branch -r | sed 's|origin/||' | sed 's|^[[:space:]]*||' | grep -v 'HEAD' | fzf --prompt="Select base branch: "`
   - If `fzf` is not available, print the numbered list of branches and ask the user to type the name of the branch they want to use.
   - Use the selected branch as the target base branch for all remaining steps.
4. Get today's date in `YYYY-MM-DD` format.
4. Build the new branch name:
   - If the target base branch contains a `/` (e.g. `UAT/main`), extract the part before the `/` and use it as the folder prefix: `UAT/ABC-123-YYYY-MM-DD`.
   - If the target base branch has no `/` (e.g. `develop`), use the full target name joined with a hyphen: `develop-ABC-123-YYYY-MM-DD`.
5. If a base branch was provided in $ARGUMENTS (skipping step 3), fetch the latest from origin: `git fetch origin`.
6. Create the new branch off the target base: `git checkout -b <new-branch> origin/<target-base-branch>`.
7. Push the new branch and set upstream tracking: `git push -u origin <new-branch>`.
8. Merge the original feature branch from origin into it: `git merge origin/<current-branch> --no-edit`.
   - If there are merge conflicts, list the conflicting files and stop. Tell the user to resolve the conflicts, then run `git merge --continue`, `git push`, and create the PR manually.
   - If the merge succeeds, push the result: `git push`.
9. Create a pull request using `gh pr create` targeting the base branch (`<target-base-branch>`), with:
   - Title: the new branch name
   - Body summarising what feature branch was merged and the date
10. Output the PR URL and confirm the new branch is tracking `origin/<new-branch>`.
