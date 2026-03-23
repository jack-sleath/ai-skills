# /invest-idea Evaluation Criteria

You are scoring the output of the `/invest-idea` skill. This skill takes a software idea, asks clarifying questions, then generates an `ACCEPTANCE_CRITERIA.md` and `MILESTONES.md` file.

For this evaluation, the skill was run in **non-interactive mode** — it could not ask the user follow-up questions, so be lenient on gaps that would normally be filled by user responses. Score based on how well it used the information available in the fixture inputs.

Score each dimension from 1 (poor) to 5 (excellent).

## Dimensions

### 1. Acceptance Criteria Structure
Does the ACCEPTANCE_CRITERIA.md follow the required template: Overview, Target User, Tech Stack, Functional Requirements, Non-Functional Requirements, Out of Scope?

- 5 = All sections present, correctly formatted, in the right order
- 3 = Most sections present but one or two missing or misnamed
- 1 = Template not followed; major sections missing or structure unrecognisable

### 2. Milestones Structure
Does the MILESTONES.md follow the required template: Tech Stack header, then numbered milestones with Goal, Tasks, and Done When?

- 5 = All milestones follow the exact format with checkboxes in "Done when", Tech Stack header present
- 3 = Mostly correct but some milestones miss a field or checkboxes are absent
- 1 = Template not followed; milestones are just bullet lists or freeform text

### 3. Milestone Granularity
Are milestones appropriately scoped — small enough to complete in a focused session, independently testable?

- 5 = Each milestone is a clear, deliverable increment; Milestone 1 is a working skeleton; later ones build incrementally
- 3 = Milestones are reasonable but some are too large or too vague to verify completion
- 1 = Milestones are either too coarse (3 massive chunks) or too fine (20 trivial steps)

### 4. Content Accuracy
Are the requirements and milestones grounded in the provided idea, with no hallucinated features?

- 5 = Every requirement traces back to the input; no invented features; placeholders used for unknowns
- 3 = Mostly faithful but adds a few assumptions not supported by the input
- 1 = Significant hallucination — features or constraints that contradict or go far beyond the input

### 5. Done-When Specificity
Are the "Done when" criteria concrete and verifiable, not vague?

- 5 = Each criterion is a testable statement (e.g. "App starts and returns 200 on /health")
- 3 = Mix of specific and vague criteria (e.g. "Basic functionality works")
- 1 = Criteria are all vague or just restate the goal

### 6. Conciseness
Is the output tight and free of filler?

- 5 = No unnecessary preamble, requirements are crisp one-liners, no padding
- 3 = Some verbose descriptions but mostly on-point
- 1 = Bloated with unnecessary explanation, repeated information, or marketing language

## Output Format

Respond with ONLY a JSON object, no other text:

```json
{
  "acceptance_criteria_structure": { "score": 1, "reasoning": "" },
  "milestones_structure": { "score": 1, "reasoning": "" },
  "milestone_granularity": { "score": 1, "reasoning": "" },
  "content_accuracy": { "score": 1, "reasoning": "" },
  "done_when_specificity": { "score": 1, "reasoning": "" },
  "conciseness": { "score": 1, "reasoning": "" },
  "total": 6,
  "max_possible": 30,
  "suggestions": []
}
```
