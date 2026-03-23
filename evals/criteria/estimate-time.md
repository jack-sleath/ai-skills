# /estimate-time Evaluation Criteria

You are scoring the output of the `/estimate-time` skill. This skill analyses git log output to estimate how much time has been spent on a project, grouping commits into work sessions and breaking down by contributor.

For this evaluation, the skill was run in **non-interactive mode** — it could not run actual git commands, so git log output was provided as a fixture file. Score based on how well it analysed the provided log data.

Score each dimension from 1 (poor) to 5 (excellent).

## Dimensions

### 1. Session Grouping
Are commits correctly grouped into work sessions (commits within ~2 hours of each other)?

- 5 = All sessions are logically grouped; gaps > 2h start new sessions; no commits misassigned
- 3 = Most groupings correct but one or two sessions split or merged incorrectly
- 1 = No meaningful grouping; treats every commit as separate or lumps everything together

### 2. Duration Estimation
Are session durations reasonable — using timestamp windows plus ~30min setup, and ~30-45min for isolated commits?

- 5 = Durations follow the stated methodology consistently; isolated commits get 30-45min
- 3 = Methodology mostly followed but some sessions have unexplained durations
- 1 = Durations appear arbitrary or methodology not applied

### 3. Contributor Breakdown
Is the output broken down by contributor with per-person sessions and estimated hours?

- 5 = Each contributor listed separately with their sessions, hours, and commit counts
- 3 = Contributors listed but breakdown is incomplete (e.g. missing session detail)
- 1 = No per-contributor breakdown; only a single total shown

### 4. Content Accuracy
Are the numbers consistent — do session hours add up to totals, are commit counts correct?

- 5 = All arithmetic is correct; session totals match per-contributor totals match overall total
- 3 = Minor arithmetic error (off by < 1 hour) but methodology is sound
- 1 = Numbers don't add up or contradict each other significantly

### 5. Caveats and Limitations
Does the output note relevant caveats (timezone issues, merge commits, estimation uncertainty)?

- 5 = Notes at least 2 relevant caveats specific to the data (e.g. "3 merge commits excluded", "all commits in same timezone")
- 3 = Generic caveat mentioned but not tailored to the actual data
- 1 = No caveats mentioned at all

### 6. Conciseness
Is the output clear and scannable without unnecessary filler?

- 5 = Clean table or structured output; no verbose prose; easy to scan
- 3 = Readable but includes some unnecessary explanation or repetition
- 1 = Wall of text, hard to find the key numbers, or excessive preamble

## Output Format

Respond with ONLY a JSON object, no other text:

```json
{
  "session_grouping": { "score": 1, "reasoning": "" },
  "duration_estimation": { "score": 1, "reasoning": "" },
  "contributor_breakdown": { "score": 1, "reasoning": "" },
  "content_accuracy": { "score": 1, "reasoning": "" },
  "caveats_and_limitations": { "score": 1, "reasoning": "" },
  "conciseness": { "score": 1, "reasoning": "" },
  "total": 6,
  "max_possible": 30,
  "suggestions": []
}
```
