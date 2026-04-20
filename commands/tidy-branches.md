Switch to the main (or master) branch, fetch the latest from origin, and delete all local branches that have been pushed to the remote.

**Steps:**

1. Detect the default branch: check if `main` exists locally or on origin, otherwise fall back to `master`. If neither exists, stop and tell the user.
2. Switch to the default branch: `git checkout <default-branch>`.
3. Fetch the latest: `git fetch origin --prune && git pull --ff-only`.
4. List all local branches except the default branch.
   - If there are none, report "no other local branches" and stop.
5. For each local branch, check if it has a corresponding remote tracking branch on origin:
   ```
   git ls-remote --heads origin <branch>
   ```
   - If the remote branch **exists**, the branch has been pushed — mark it for deletion.
   - If the remote branch **does not exist**, keep it (it is local-only work that hasn't been pushed yet).
6. Delete all branches marked for deletion: `git branch -D <branch1> <branch2> ...`.
7. Report a summary:
   - Deleted branches (list).
   - Kept branches (local-only, not yet pushed) (list).
   - If nothing was deleted, say so.

**Rules:**
- Never delete the default branch.
- Never push or touch the remote — this is local cleanup only.
- If a branch cannot be deleted (e.g. checked out in another worktree), report the error and continue with the rest.
