Create a staging branch off a target base branch, then merge the current feature branch into it.

Arguments: $ARGUMENTS
- Required: the target base branch (e.g. `UAT/main`, `staging/main`)

**Steps:**

1. Run `git branch --show-current` to get the current branch name.
2. Extract the ticket identifier from the current branch name — assume the branch name is `<prefix>/<IDENTIFIER>` and the identifier is everything after the first `/`. If the branch doesn't follow this pattern, stop and tell the user.
3. Get today's date in `YYYY-MM-DD` format.
4. Build the new branch name:
   - If the target base branch contains a `/` (e.g. `UAT/main`), extract the part before the `/` and use it as the folder prefix: `UAT/ABC-123-YYYY-MM-DD`.
   - If the target base branch has no `/` (e.g. `develop`), use the full target name joined with a hyphen: `develop-ABC-123-YYYY-MM-DD`.
5. Fetch the latest from origin: `git fetch origin`.
6. Create the new branch off the target base: `git checkout -b <new-branch> origin/<target-base-branch>`.
7. Push the new branch and set upstream tracking: `git push -u origin <new-branch>`.
8. Merge the original feature branch from origin into it: `git merge origin/<current-branch> --no-edit`.
   - If there are merge conflicts, list the conflicting files and stop. Tell the user to resolve the conflicts, then run `git merge --continue` and `git push`.
   - If the merge succeeds, push the result: `git push`.
9. Report the new branch name and confirm it is tracking `origin/<new-branch>`.
