Fetch a branch from origin and merge it into the current active branch.

Arguments: $ARGUMENTS
- Required: the name of the branch from origin to merge in (e.g. `feature/ABC-123`, `main`).

**Steps:**

1. If no branch name was provided in $ARGUMENTS, use the same branch-selection logic as step 3 of `/branch-for` — fetch origin, list remote branches, use `fzf` if available, otherwise print a numbered list and ask the user to choose. Use the selected branch as the source branch for all remaining steps.
2. Run `git branch --show-current` to confirm the current active branch. Tell the user which branch will receive the merge.
3. Fetch the latest from origin (if not already done): `git fetch origin`.
4. Merge the source branch from origin into the current branch: `git merge origin/<source-branch> --no-edit`.
   - If there are merge conflicts, list the conflicting files and stop. Tell the user to resolve the conflicts and then run `git merge --continue`.
   - If the merge succeeds, confirm to the user that `origin/<source-branch>` has been merged into the current branch.
