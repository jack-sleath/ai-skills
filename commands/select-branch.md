Interactively select a branch from the remote and return its name.

Arguments: $ARGUMENTS
- Optional: a prompt label to display (e.g. `"Select base branch"`, `"Select branch to merge"`). Defaults to `"Select branch"` if not provided.

**Steps:**

1. Fetch the latest from origin: `git fetch origin`.
2. List all remote branches: `git branch -r | sed 's|origin/||' | sed 's|^[[:space:]]*||' | grep -v 'HEAD'`
3. Check if `fzf` is available: `command -v fzf`
   - If available, pipe the branch list into it: `git branch -r | sed 's|origin/||' | sed 's|^[[:space:]]*||' | grep -v 'HEAD' | fzf --prompt="<label>: "`
   - If not available, print the numbered list of branches and ask the user to type the name of the branch they want.
4. Return the selected branch name for use in the calling skill.
