Find the milestones file in this project (look for files named MILESTONES.md, milestones.md, MILESTONES.txt, or similar in the project root or docs/ folder) and implement the next incomplete milestone by following these rules:

**Rules:**

1. **Work one milestone at a time.** Find the lowest-numbered milestone that is not yet complete and implement only that milestone. Do not build ahead.
2. **Verify the "Done when" criteria before marking a milestone complete.** If the criteria are not met, keep working on the current milestone.
3. **Do not invent behaviour that is not specified.** If something is unclear, implement the simplest reasonable interpretation and add a comment flagging the assumption.
4. **At the start of each milestone, create a new git branch** using the name from the milestone's `**Branch:**` field if one is present (e.g. `milestone-5-dark-mode`), otherwise default to `milestone-N` (e.g. `milestone-3`). **Branch off the previous milestone's branch** so that each milestone builds on the last. If this is the first milestone, branch off the current branch. When the "Done when" criteria are met, commit all changes with a descriptive message summarising what the milestone added and why, then push the branch to the remote.

**Steps to follow:**

1. Read the milestones file and identify the lowest-numbered incomplete milestone.
2. Determine the parent branch: find the previous milestone's branch (by its `**Branch:**` field or the `milestone-(N-1)` convention). If it exists locally or on the remote, use it as the base. If this is the first milestone or no previous branch exists, use the current branch as the base.
3. Check out a new branch from the parent branch. Use the name from the milestone's `**Branch:**` field if present; otherwise use `milestone-N` (e.g. `git checkout -b milestone-N <parent-branch>`).
4. Read any relevant existing code to understand the current state before making changes.
5. Implement the milestone — make only the changes required by this milestone's spec.
6. Before verifying criteria, discover any test or build commands for this project by checking (in order): `package.json` scripts, `Makefile` targets, `README` instructions, CI config files (`.github/workflows`, `azure-pipelines.yml`, etc.), and common conventions (`pytest`, `dotnet test`, `cargo test`, `go test ./...`). Use what you find to inform how to validate the milestone.
7. Verify every "Done when" criterion is satisfied. Run any tests or checks specified. If criteria are not met, continue working.
8. If test or build commands were found in step 6, run them now. If any fail, fix the issues before proceeding.
9. Once all criteria are met and checks pass, stage and commit all changes with a message of the form: `milestone N: <short summary of what was added and why>`.
10. Push the branch to the remote.
11. Update the milestones file to mark this milestone as complete (e.g. add a `[x]` or `✅` marker).
12. Commit and push the milestones file update on the same branch.
13. Report which milestone was completed, what was done, and what checks were run.
