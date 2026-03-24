# /feedback Evaluation Criteria

You are scoring the output of the `/feedback` skill. This skill translates feedback or a change request into a concrete plan by appending new sections to `ACCEPTANCE_CRITERIA.md`, appending new milestones to `MILESTONES.md`, and creating a `<CHANGE-TITLE>_FEATURE.md` file.

For this evaluation, the skill was run in **non-interactive mode** — it could not ask the user follow-up questions. The fixture provides a complete change request alongside existing ACCEPTANCE_CRITERIA.md and MILESTONES.md files, so be lenient on the interactive question phase but evaluate the quality of all three outputs.

Score each dimension from 1 (poor) to 10 (excellent).

## Dimensions

### 1. Acceptance Criteria Append
Whether a new "Change Request" section is correctly appended to ACCEPTANCE_CRITERIA.md with Overview, Raised By, Functional Requirements, Non-Functional Requirements, and Out of Scope.

- 10 = New section appended with all required sub-sections; functional requirements are numbered "The system must..." statements covering all aspects of the change request (due date field, overdue indicator, overdue endpoint, email digest readiness)
- 5 = Section appended but missing one sub-section or requirements don't fully cover the change request
- 1 = No new section appended, or it overwrites the existing content rather than appending

### 2. Milestone Continuation
Whether new milestones are appended to MILESTONES.md with correct numbering, continuing from the highest existing milestone.

- 10 = New milestones start at Milestone 3 (continuing from existing Milestone 2); each has Branch, Goal, Tasks, and Done-when; headings tagged with [change-title]; branch names follow the `milestone-N-<change-title>` convention
- 5 = Milestones appended but numbering is wrong, tags are missing, or one milestone lacks required fields
- 1 = No milestones appended, numbering restarts at 1, or existing milestones are overwritten

### 3. Feature File Generation
Whether a `<CHANGE-TITLE>_FEATURE.md` file is generated following the /feature template, scoped only to the new change request.

- 10 = Feature file created with correct filename convention; content sources only from the new change request section and new milestones — not from pre-existing acceptance criteria or milestones
- 5 = Feature file created but includes content from existing (non-change-request) sections, or filename convention is wrong
- 1 = No feature file generated, or it's a copy of the full acceptance criteria

### 4. Content Accuracy
Whether all three outputs are faithful to the change request fixture without hallucination.

- 10 = All requirements, constraints, and scope trace back to the change request fixture (due dates, overdue indicator, API endpoint, email digest, no status workflow changes, JWT auth compatibility)
- 5 = Mostly accurate but one or two details are embellished beyond the fixture
- 1 = Significant hallucination — requirements or features not in the change request

### 5. Milestone Granularity
Whether the new milestones are appropriately sized and sequenced for incremental delivery of the change.

- 10 = 2–4 new milestones, each independently testable; first milestone lays groundwork (data model + migration); later milestones build incrementally; final milestone satisfies all new requirements
- 5 = Milestones exist but are too coarse (everything in one) or too fine (trivial steps)
- 1 = Only one milestone covering the entire change, or milestone sequence doesn't make logical sense

### 6. Done-When Specificity
Whether done-when criteria in the new milestones are concrete and verifiable.

- 10 = Every criterion is specific and testable (e.g. "PATCH /tasks/:id accepts optional due_date field", "GET /tasks/overdue returns only non-done tasks past their due date")
- 5 = Most criteria are specific but a few are vague
- 1 = Criteria are vague ("feature works", "due dates are supported") or missing

### 7. Conciseness
Whether all outputs are appropriately tight without filler or meta-commentary.

- 10 = Requirements are one-line statements; milestones are focused; feature file is proportionate; no commentary about the generation process
- 5 = Mostly concise but some sections are verbose
- 1 = Significant filler, redundancy, or meta-commentary

## Output Format

Respond with ONLY a JSON object, no other text:

```json
{
  "acceptance_criteria_append": { "score": 0, "reasoning": "" },
  "milestone_continuation": { "score": 0, "reasoning": "" },
  "feature_file_generation": { "score": 0, "reasoning": "" },
  "content_accuracy": { "score": 0, "reasoning": "" },
  "milestone_granularity": { "score": 0, "reasoning": "" },
  "done_when_specificity": { "score": 0, "reasoning": "" },
  "conciseness": { "score": 0, "reasoning": "" },
  "total": 0,
  "max_possible": 70,
  "suggestions": []
}
```
