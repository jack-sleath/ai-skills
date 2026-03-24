# /feedback Evaluation Criteria

You are scoring the output of the `/feedback` skill. This skill translates a change request or feedback into three concrete outputs: an appendix to `ACCEPTANCE_CRITERIA.md` (new change request section), new milestones appended to `MILESTONES.md`, and a standalone `<CHANGE-TITLE>_FEATURE.md` document.

For this evaluation, the skill was run in **non-interactive mode** — it could not ask the user clarifying questions, so the change request and existing project files were provided directly. Be lenient on details that would normally come from interactive Q&A, but strict on the quality and structure of all three output documents.

Score each dimension from 1 (poor) to 5 (excellent).

## Dimensions

### 1. Structure Compliance
Do all three outputs follow their exact templates — change request section in ACCEPTANCE_CRITERIA.md, milestones in MILESTONES.md (continuing numbering), and a FEATURE.md file?

- 5 = All three outputs present with correct headings, ordering, and formatting; milestone numbering continues from where the existing file left off
- 3 = All three present but one has a missing section or wrong milestone numbering
- 1 = One or more outputs missing entirely, or templates not followed

### 2. Requirement Extraction
Are the functional requirements in the change request section complete, specific, and traceable to the provided feedback?

- 5 = Every requirement maps to the input feedback; requirements are "The system must..." / "The user can..." format; nothing significant omitted
- 3 = Most requirements captured but one or two are vague or a key aspect of the feedback is missing
- 1 = Requirements are generic, miss the main ask, or hallucinate features not in the feedback

### 3. Milestone Granularity
Are the new milestones appropriately scoped — small enough for a focused work session, independently testable, and building incrementally toward the full change?

- 5 = Each milestone is a clear, independently deployable/testable unit; first milestone lays groundwork; final milestone completes all new requirements; milestones are small and focused
- 3 = Milestones are present and sequential but one is too large or two could be merged without loss
- 1 = Single monolithic milestone, or milestones don't build incrementally, or scope doesn't cover the full change

### 4. Done-When Specificity
Are the "Done when" criteria on each milestone concrete and verifiable, not vague or process-oriented?

- 5 = Every criterion is a specific, checkable condition (e.g. "GET /items returns 200 with list of items"); no "code reviewed" or "looks good" criteria
- 3 = Most criteria are concrete but one or two are vague (e.g. "feature works correctly")
- 1 = Criteria are all vague, untestable, or missing entirely

### 5. Content Accuracy
Is all output faithful to the provided input files and feedback, with no hallucinated features, endpoints, or requirements?

- 5 = Every claim traces to the fixture input; no invented behaviour or references to non-existent code
- 3 = Mostly faithful but one or two details appear assumed rather than evidenced
- 1 = Multiple fabricated requirements or references to things not in the input

### 6. Conciseness
Is the output tight and free of filler across all three documents?

- 5 = No unnecessary preamble, no redundant content between documents, every section adds distinct value
- 3 = Some redundancy between the FEATURE.md and other outputs, or minor filler
- 1 = Verbose, repetitive, or padded with unnecessary explanation

## Output Format

Respond with ONLY a JSON object, no other text:

```json
{
  "structure_compliance": { "score": 1, "reasoning": "" },
  "requirement_extraction": { "score": 1, "reasoning": "" },
  "milestone_granularity": { "score": 1, "reasoning": "" },
  "done_when_specificity": { "score": 1, "reasoning": "" },
  "content_accuracy": { "score": 1, "reasoning": "" },
  "conciseness": { "score": 1, "reasoning": "" },
  "total": 6,
  "max_possible": 30,
  "suggestions": []
}
```
