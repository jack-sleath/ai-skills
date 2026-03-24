# /invest-idea Evaluation Criteria

You are scoring the output of the `/invest-idea` skill. This skill takes a software idea and fleshes it out into two concrete output files: `ACCEPTANCE_CRITERIA.md` and `MILESTONES.md`, after gathering requirements through clarifying questions.

For this evaluation, the skill was run in **non-interactive mode** — it could not ask the user follow-up questions. The fixture provides a pre-answered idea brief, so be lenient if the skill didn't ask clarifying questions and instead derived answers from the provided context. Focus on the quality of the two output files.

Score each dimension from 1 (poor) to 10 (excellent).

## Dimensions

### 1. Acceptance Criteria Structure
Whether the ACCEPTANCE_CRITERIA.md follows the specified template: Overview, Target User, Tech Stack, Functional Requirements, Non-Functional Requirements, Out of Scope.

- 10 = All sections present, correctly ordered, and properly formatted; functional requirements are numbered "The system must..." / "The user can..." statements
- 5 = Most sections present but one is missing or requirements are not in the specified format
- 1 = Output does not follow the template; major sections missing or structure is unrecognisable

### 2. Milestones Structure
Whether the MILESTONES.md follows the specified template with Tech Stack header and correctly structured milestones.

- 10 = Tech Stack header present; each milestone has Goal, Tasks, and Done-when checklist with concrete verifiable criteria; Milestone 1 is a project scaffold
- 5 = Milestones are present but missing some fields (e.g. no Done-when criteria) or Milestone 1 isn't a scaffold
- 1 = No milestone structure; output is a flat list or missing entirely

### 3. Content Accuracy
Whether the output is faithful to the idea brief without hallucinating features, tech choices, or requirements not mentioned or implied.

- 10 = All requirements, tech choices, and features trace back to the fixture input; nothing invented beyond what was stated or clearly implied
- 5 = Mostly accurate but includes one or two features or tech choices not supported by the input
- 1 = Significant hallucination — multiple requirements or features that contradict or go well beyond the input

### 4. Requirement Completeness
Whether all features and constraints from the idea brief are captured in the functional and non-functional requirements.

- 10 = Every feature mentioned in the fixture (item listing, borrowing, messaging, lending ledger, auth, image upload, mobile-friendly, email notifications) appears as a requirement
- 5 = Most features captured but one or two are missing
- 1 = Fewer than half the stated features appear in the requirements

### 5. Milestone Granularity
Whether milestones are appropriately sized and sequenced for incremental delivery.

- 10 = 4–8 milestones, each independently testable, building incrementally; small enough for a focused work session; the final milestone satisfies all acceptance criteria
- 5 = Milestones exist but some are too large (multiple features bundled) or too small (trivial single-line tasks)
- 1 = Only 1–2 milestones covering everything, or 15+ milestones that are trivially small

### 6. Done-When Specificity
Whether done-when criteria are concrete, verifiable statements rather than vague descriptions.

- 10 = Every done-when criterion is a specific, testable condition (e.g. "POST /items returns 201 with the created item") — no vague criteria like "feature works correctly"
- 5 = Most criteria are specific but a few are vague or untestable
- 1 = Criteria are mostly vague ("app works", "feature is complete") or missing entirely

### 7. Conciseness
Whether the output is appropriately tight without filler or unnecessary commentary.

- 10 = Both files are focused and proportionate; no meta-commentary about the generation process; no padding
- 5 = Mostly concise but some sections are verbose or repetitive
- 1 = Significant filler, redundancy, or meta-commentary

## Output Format

Respond with ONLY a JSON object, no other text:

```json
{
  "acceptance_criteria_structure": { "score": 0, "reasoning": "" },
  "milestones_structure": { "score": 0, "reasoning": "" },
  "content_accuracy": { "score": 0, "reasoning": "" },
  "requirement_completeness": { "score": 0, "reasoning": "" },
  "milestone_granularity": { "score": 0, "reasoning": "" },
  "done_when_specificity": { "score": 0, "reasoning": "" },
  "conciseness": { "score": 0, "reasoning": "" },
  "total": 0,
  "max_possible": 70,
  "suggestions": []
}
```
