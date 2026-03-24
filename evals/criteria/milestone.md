# /milestone Evaluation Criteria

You are scoring the output of the `/milestone` skill. This skill reads a MILESTONES.md file, identifies the next incomplete milestone, creates a git branch, implements the milestone, verifies done-when criteria, and commits the result.

For this evaluation, the skill was run in **non-interactive mode** — it could not ask the user follow-up questions. The fixture provides a MILESTONES.md with completed and incomplete milestones. Since the skill normally runs git commands and builds/tests code, be lenient on actual git operations and focus on whether the skill correctly identifies the next milestone, plans the right implementation, and follows the process rules.

Score each dimension from 1 (poor) to 10 (excellent).

## Dimensions

### 1. Milestone Identification
Whether the skill correctly identifies the lowest-numbered incomplete milestone and does not skip ahead or re-implement a completed one.

- 10 = Correctly identifies Milestone 1 (Recipe CRUD API) as the next incomplete milestone; does not attempt Milestone 0 (completed) or Milestone 2
- 5 = Identifies the right milestone but also partially works on the next one, or hesitates about which to pick
- 1 = Picks the wrong milestone, attempts a completed milestone, or tries to implement multiple milestones

### 2. Branch Strategy
Whether the skill creates the correct branch from the correct parent, following the naming convention.

- 10 = Creates branch `milestone-1-recipe-crud` (from the Branch field); bases it on the previous milestone's branch or current branch as specified
- 5 = Creates a branch but uses the wrong name or bases it on the wrong parent
- 1 = Does not create a branch, or uses an unrelated branch name

### 3. Implementation Scope
Whether the implementation is limited to what the milestone specifies — no building ahead, no skipping tasks.

- 10 = Implements exactly what Milestone 1 specifies: Prisma schema, migration, all 5 CRUD endpoints, validation, and integration tests — nothing from Milestone 2
- 5 = Implements the core of the milestone but misses one task or includes something from a later milestone
- 1 = Implements only a fraction of the milestone, or builds significant functionality from future milestones

### 4. Done-When Verification
Whether the skill verifies each done-when criterion before considering the milestone complete.

- 10 = Explicitly checks each criterion: POST returns 201/400, GET returns paginated results with default page size 20, GET/:id returns 200/404, PUT returns 200/404 with validation, DELETE returns 204/404, tests pass via `npm test`
- 5 = Verifies most criteria but skips one or two, or verification is implicit rather than explicit
- 1 = No verification of done-when criteria; just implements and commits

### 5. Build/Test Discovery
Whether the skill discovers and uses the project's test/build commands as specified in step 6 of the skill.

- 10 = Checks package.json scripts, identifies the test command, and runs it; also looks for CI config or other build tools
- 5 = Runs tests but doesn't discover the command from project files (e.g. assumes `npm test` without checking)
- 1 = Does not run any tests or build commands

### 6. Content Accuracy
Whether the implemented code and configuration match what the milestone specifies, with no hallucinated requirements.

- 10 = Prisma schema matches specified columns exactly; endpoints match specified routes and behaviours; validation rules match spec (title required, servings > 0)
- 5 = Most implementation is accurate but one detail deviates from the spec
- 1 = Implementation significantly deviates from the milestone spec or includes invented requirements

### 7. Conciseness
Whether the output communication is focused — reports what was done without excessive commentary.

- 10 = Reports: which milestone was completed, what was implemented, what checks were run — nothing more
- 5 = Mostly focused but includes some unnecessary narration about the process
- 1 = Verbose play-by-play of every decision, or excessive meta-commentary

## Output Format

Respond with ONLY a JSON object, no other text:

```json
{
  "milestone_identification": { "score": 0, "reasoning": "" },
  "branch_strategy": { "score": 0, "reasoning": "" },
  "implementation_scope": { "score": 0, "reasoning": "" },
  "done_when_verification": { "score": 0, "reasoning": "" },
  "build_test_discovery": { "score": 0, "reasoning": "" },
  "content_accuracy": { "score": 0, "reasoning": "" },
  "conciseness": { "score": 0, "reasoning": "" },
  "total": 0,
  "max_possible": 70,
  "suggestions": []
}
```
