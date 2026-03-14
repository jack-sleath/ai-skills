Find the milestones file in this project (look for files named MILESTONES.md, milestones.md, MILESTONES.txt, or similar in the project root or docs/ folder) and implement the next incomplete milestone by following these rules:

**Rules:**

1. **Work one milestone at a time.** Find the lowest-numbered milestone that is not yet complete and implement only that milestone. Do not build ahead.
2. **Verify the "Done when" criteria before marking a milestone complete.** If the criteria are not met, keep working on the current milestone.
3. **Do not invent behaviour that is not specified.** If something is unclear, implement the simplest reasonable interpretation and add a comment flagging the assumption.
4. **At the start of each milestone, create a new git branch** named `milestone-N` (e.g. `milestone-3`), tracking the same upstream as the current branch. When the "Done when" criteria are met, commit all changes with a descriptive message summarising what the milestone added and why, then push the branch to the remote.

**Steps to follow:**

1. Read the milestones file and identify the lowest-numbered incomplete milestone.
2. Check out a new branch named `milestone-N` from the current branch, tracking the same upstream (e.g. `git checkout -b milestone-N`).
3. Read any relevant existing code to understand the current state before making changes.
4. Implement the milestone — make only the changes required by this milestone's spec.
5. Before verifying criteria, discover any test or build commands for this project by checking (in order): `package.json` scripts, `Makefile` targets, `README` instructions, CI config files (`.github/workflows`, `azure-pipelines.yml`, etc.), and common conventions (`pytest`, `dotnet test`, `cargo test`, `go test ./...`). Use what you find to inform how to validate the milestone.
6. Verify every "Done when" criterion is satisfied. Run any tests or checks specified. If criteria are not met, continue working.
7. If test or build commands were found in step 5, run them now. If any fail, fix the issues before proceeding.
8. Once all criteria are met and checks pass, stage and commit all changes with a message of the form: `milestone N: <short summary of what was added and why>`.
9. Push the branch to the remote.
10. Update the milestones file to mark this milestone as complete (e.g. add a `[x]` or `✅` marker).
11. Commit and push the milestones file update on the same branch.
12. Report which milestone was completed, what was done, and what checks were run.
