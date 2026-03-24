# /milestone Evaluation Criteria

You are scoring the output of the `/milestone` skill. This skill reads a milestones file, identifies the lowest-numbered incomplete milestone, creates a branch, implements the milestone, verifies "Done when" criteria, commits, and pushes.

For this evaluation, the skill was run in **non-interactive mode** — it could not run actual git commands or execute builds/tests. Score based on the implementation plan it describes, the code changes it proposes, and how well it follows the milestone spec, not on whether git/build operations succeeded.

Score each dimension from 1 (poor) to 5 (excellent).

## Dimensions

### 1. Milestone Identification
Does it correctly identify the lowest-numbered incomplete milestone and only work on that one?

- 5 = Correctly identifies the next incomplete milestone by number; does not skip ahead or work on multiple milestones
- 3 = Identifies the correct milestone but also partially addresses a later one, or is ambiguous about which milestone it's working on
- 1 = Works on the wrong milestone, skips one, or tries to implement multiple at once

### 2. Branch Strategy
Does it follow the branching rules — using the milestone's Branch field if present, branching off the previous milestone's branch?

- 5 = Uses exact branch name from the milestone spec; correctly identifies and branches from the previous milestone's branch (or current branch for first milestone)
- 3 = Creates a branch but uses a generic name instead of the specified one, or branches from the wrong base
- 1 = No branch created, or branching strategy is completely wrong

### 3. Implementation Completeness
Does the proposed implementation cover all tasks listed in the milestone spec?

- 5 = Every task in the milestone's task list is addressed with specific code changes or actions; nothing omitted
- 3 = Most tasks addressed but one is missed or only partially implemented
- 1 = Multiple tasks missing, or implementation is superficial / placeholder-only

### 4. Done-When Verification
Does it verify each "Done when" criterion and demonstrate they are met?

- 5 = Explicitly checks every "Done when" criterion; describes how each is satisfied; runs any relevant tests or checks
- 3 = Mentions done-when criteria but doesn't verify all of them, or verification is hand-wavy
- 1 = Ignores done-when criteria entirely, or claims they're met without evidence

### 5. Content Accuracy
Are the proposed changes faithful to the milestone spec, with no invented requirements or scope creep?

- 5 = All changes trace directly to the milestone spec; no gold-plating or features not specified
- 3 = Mostly on-spec but adds one minor thing not requested, or misinterprets a requirement slightly
- 1 = Significant scope creep, hallucinated requirements, or misunderstood spec

### 6. Conciseness
Is the output tight — focused on what was done and why, without unnecessary explanation?

- 5 = Clean, direct reporting of actions taken and criteria verified; no filler
- 3 = Some unnecessary explanation or preamble but mostly on-point
- 1 = Verbose, repetitive, or padded with unnecessary commentary

## Output Format

Respond with ONLY a JSON object, no other text:

```json
{
  "milestone_identification": { "score": 1, "reasoning": "" },
  "branch_strategy": { "score": 1, "reasoning": "" },
  "implementation_completeness": { "score": 1, "reasoning": "" },
  "done_when_verification": { "score": 1, "reasoning": "" },
  "content_accuracy": { "score": 1, "reasoning": "" },
  "conciseness": { "score": 1, "reasoning": "" },
  "total": 6,
  "max_possible": 30,
  "suggestions": []
}
```
