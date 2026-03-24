# /audit Evaluation Criteria

You are scoring the output of the `/audit` skill. This skill reverse-engineers documentation from an existing codebase, producing an `ACCEPTANCE_CRITERIA.md` and a `MILESTONES.md` (starting at Milestone 0) that describe what the project currently does, derived from Swagger/OpenAPI definitions, unit tests, and any Gherkin scenarios.

For this evaluation, the skill was run in **non-interactive mode** — it could not ask the user follow-up questions about solution scope, missing Swagger files, or Gherkin input. Be lenient on questions it would normally ask interactively, but strict on the quality of the output documents it generates.

Score each dimension from 1 (poor) to 5 (excellent).

## Dimensions

### 1. Structure Compliance
Do both output files follow the exact templates specified in the skill (ACCEPTANCE_CRITERIA.md and MILESTONES.md with all required sections)?

- 5 = Both files present with all required sections in the correct order; headings, note block, and formatting match the template exactly
- 3 = Both files present but one or two sections missing or out of order (e.g. no Coverage Gaps, or Tech Stack omitted)
- 1 = Template not followed; output is freeform or one file is missing entirely

### 2. Swagger Coverage
Does the ACCEPTANCE_CRITERIA.md accurately document the API surface from the provided Swagger/controller input?

- 5 = All endpoints listed with correct HTTP methods, paths, and summaries grouped by controller/tag; nothing omitted or fabricated
- 3 = Most endpoints captured but some missing or summaries are vague; grouping is present but inconsistent
- 1 = Major endpoints missing, methods wrong, or API Surface section absent

### 3. Content Accuracy
Are the functional requirements, test coverage summary, and other derived content faithful to the input, with no hallucinated behaviour?

- 5 = Every requirement traces to something in the Swagger, tests, or Gherkin input; no invented behaviour
- 3 = Mostly faithful but one or two requirements appear assumed rather than evidenced
- 1 = Multiple hallucinated requirements or claims about the codebase that are not in the fixtures

### 4. Milestone Quality
Does the MILESTONES.md Milestone 0 accurately summarise the current state with specific, verifiable "Done when" criteria?

- 5 = Milestone 0 has a clear goal, accurate "What exists" summary, API surface summary, test coverage summary, known gaps, and concrete done-when checkboxes; Milestone 1 placeholder present
- 3 = Milestone 0 present but light on detail — missing one of: API summary, test summary, or gaps; done-when criteria are vague
- 1 = No Milestone 0, or it is a generic placeholder with no project-specific content

### 5. Coverage Gaps Identification
Does the output identify genuine gaps, assumptions, or untested areas rather than inventing problems or ignoring obvious holes?

- 5 = Gaps listed are genuine (e.g. missing tests for specific endpoints, undocumented error codes) and actionable
- 3 = Some gaps noted but they are generic (e.g. "more tests needed") rather than specific
- 1 = No gaps section, or gaps are fabricated / clearly wrong

### 6. Conciseness
Is the output appropriately tight without filler, while still being comprehensive?

- 5 = No unnecessary preamble, no restating the obvious, every section adds distinct value
- 3 = Some redundancy between sections or minor filler text
- 1 = Verbose, repetitive, or padded with unnecessary explanation

## Output Format

Respond with ONLY a JSON object, no other text:

```json
{
  "structure_compliance": { "score": 1, "reasoning": "" },
  "swagger_coverage": { "score": 1, "reasoning": "" },
  "content_accuracy": { "score": 1, "reasoning": "" },
  "milestone_quality": { "score": 1, "reasoning": "" },
  "coverage_gaps_identification": { "score": 1, "reasoning": "" },
  "conciseness": { "score": 1, "reasoning": "" },
  "total": 6,
  "max_possible": 30,
  "suggestions": []
}
```
