# /estimate-time Evaluation Criteria

You are scoring the output of the `/estimate-time` skill. This skill analyses a project's git history to estimate how much time has been spent on it, grouping commits into work sessions and breaking down hours by contributor.

For this evaluation, the skill was run in **non-interactive mode** — it could not ask the user follow-up questions. The skill was provided with simulated `git log` output as a fixture file instead of running real git commands, so be lenient on command construction and focus on the quality of the time analysis.

Score each dimension from 1 (poor) to 10 (excellent).

## Dimensions

### 1. Session Grouping
Whether commits are correctly grouped into work sessions based on temporal proximity (~2 hours between commits).

- 10 = All sessions are correctly identified with sensible boundaries; commits within 2 hours are grouped together, gaps over 2 hours start new sessions
- 5 = Most sessions are correct but one or two groupings are debatable or inconsistent
- 1 = Sessions are not grouped at all, or grouping logic is clearly wrong (e.g. all commits in one session, or every commit is its own session)

### 2. Duration Estimation
Whether session durations are calculated correctly using timestamp windows plus reasonable overhead for setup time.

- 10 = Each session duration uses first-to-last commit window plus ~30 min setup; isolated commits estimated at 30–45 min; totals add up correctly
- 5 = Durations are roughly reasonable but setup time is inconsistent or some arithmetic is off
- 1 = Durations are wildly inaccurate, missing, or don't account for setup time at all

### 3. Contributor Breakdown
Whether the output breaks down sessions and estimated hours by individual contributor.

- 10 = Each contributor (Alice, Bob, Charlie) has their own section with sessions listed and per-person hour totals; overall total is also provided
- 5 = Contributors are identified but breakdown is incomplete (e.g. missing one contributor or no per-person totals)
- 1 = No per-contributor breakdown; only a single aggregate number

### 4. Content Accuracy
Whether the analysis is faithful to the fixture data with no hallucinated commits, contributors, or timestamps.

- 10 = Every commit, author, and timestamp referenced matches the fixture data exactly; no invented data
- 5 = Mostly accurate but one or two minor details are slightly off (e.g. a rounded timestamp)
- 1 = Contains hallucinated commits, wrong author attributions, or fabricated timestamps

### 5. Caveats and Limitations
Whether the output notes relevant caveats about the estimation methodology.

- 10 = Notes limitations such as: estimates are rough, merge commits may not represent real work, timezone assumptions, pre-first-commit work is estimated
- 5 = Mentions one or two caveats but misses obvious ones
- 1 = No caveats mentioned; presents estimates as precise facts

### 6. Structure and Readability
Whether the output is well-organised with clear headings, tables or lists, and a summary.

- 10 = Clean structure with per-contributor sections, a summary table or total, and easy-to-scan formatting
- 5 = Readable but somewhat disorganised or missing a clear summary
- 1 = Wall of text with no structure, or key information is buried

## Output Format

Respond with ONLY a JSON object, no other text:

```json
{
  "session_grouping": { "score": 0, "reasoning": "" },
  "duration_estimation": { "score": 0, "reasoning": "" },
  "contributor_breakdown": { "score": 0, "reasoning": "" },
  "content_accuracy": { "score": 0, "reasoning": "" },
  "caveats_and_limitations": { "score": 0, "reasoning": "" },
  "structure_and_readability": { "score": 0, "reasoning": "" },
  "total": 0,
  "max_possible": 60,
  "suggestions": []
}
```
