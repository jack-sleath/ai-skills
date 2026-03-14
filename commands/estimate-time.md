Analyse this project's git history to estimate how much time has been spent on it.

Run: git log --format="%ai %ae %an %s" --all

Then:
1. Group commits into work sessions — treat commits within ~2 hours of each other as one session
2. For each session, estimate duration using the timestamp window (first to last commit), adding ~30 min for setup/work before the first commit
3. For single isolated commits, assume ~30–45 min of work
4. Break down by contributor, showing their sessions and estimated hours separately
5. Summarise total estimated hours per person and overall

Note any caveats (e.g. timezone differences, merge commits that don't represent real work, etc.)
