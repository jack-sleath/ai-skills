Analyse this project's git history to estimate how much time has been spent on it.

Arguments (optional): $ARGUMENTS

Interpret the argument as one of the following:
- No arguments: include all commits.
- A relative period like `3 months`, `6 months`, `30 days`, `1 year`, `2 weeks` etc. — calculate the start date by subtracting that period from today's date, then include commits on or after that date.
- A single date (e.g. `2026-03-01`) — include commits on or after that date.
- Two dates (e.g. `2026-03-01 2026-03-14`) — include commits within that range (inclusive).

Build the git log command accordingly:
- No args: `git log --format="%ai %ae %an %s" --all`
- Start date only: `git log --format="%ai %ae %an %s" --all --after="START_DATE"`
- Start and end date: `git log --format="%ai %ae %an %s" --all --after="START_DATE" --before="END_DATE"`

Then:
1. Group commits into work sessions — treat commits within ~2 hours of each other as one session
2. For each session, estimate duration using the timestamp window (first to last commit), adding ~30 min for setup/work before the first commit
3. For single isolated commits, assume ~30–45 min of work
4. Break down by contributor, showing their sessions and estimated hours separately
5. Summarise total estimated hours per person and overall

Note any caveats (e.g. timezone differences, merge commits that don't represent real work, etc.)
