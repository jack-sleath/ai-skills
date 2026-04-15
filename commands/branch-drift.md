Check all repositories in the current org/user for branches that have drifted ahead of their expected downstream branch. Report any repos where:

- `main` or `master` is ahead of `develop`
- A release branch (any branch matching `release/*` or `release-*`) is ahead of `main` or `master`
- `develop` is ahead of `UAT/main`

**Steps:**

1. Determine the owner of the current repository by running `gh repo view --json owner --jq .owner.login`.
   - If `gh` is not available or the command fails, stop and tell the user to install/authenticate the GitHub CLI.

2. List all non-archived repositories in that org/user by running `gh repo list <owner> --no-archived --limit 200 --json name,defaultBranch`.

3. For each repository, check for drift by comparing branches. Use `gh api repos/<owner>/<repo>/compare/<base>...<head> --jq .ahead_by` for each comparison. If a branch doesn't exist in a repo, skip that comparison silently.

   Check these comparisons:
   a. **main/master ahead of develop** — compare `develop...<defaultBranch>`. Only check if `develop` exists in the repo.
   b. **Release branches ahead of main/master** — first list branches matching `release/*` or `release-*` using `gh api repos/<owner>/<repo>/branches --jq '.[].name' | grep -E '^release[/-]'`. For each match, compare `<defaultBranch>...<releaseBranch>`.
   c. **develop ahead of UAT/main** — compare `UAT/main...develop`. Only check if both `develop` and `UAT/main` exist in the repo.

4. Only report comparisons where `ahead_by` is greater than 0. Present the results as a grouped list:

   ### main/master ahead of develop
   - **<repo>** — <N> commits ahead

   ### Release branches ahead of main/master
   - **<repo>** `<release-branch>` — <N> commits ahead

   ### develop ahead of UAT/main
   - **<repo>** — <N> commits ahead

   - Omit any section where no repos have drift.
   - If nothing is drifting anywhere, say: **All branches are in sync across <owner>.**

5. After the list, show a summary line:
   > **X repos with drift across <owner>**
