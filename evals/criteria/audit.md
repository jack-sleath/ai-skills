# /audit Evaluation Criteria

You are scoring the output of the `/audit` skill. This skill reverse-engineers documentation for an existing codebase by analysing Swagger/OpenAPI definitions and unit tests to produce an `ACCEPTANCE_CRITERIA.md` and a `MILESTONES.md` (starting at Milestone 0) that describe what the project currently does.

For this evaluation, the skill was run in **non-interactive mode** — it could not ask the user follow-up questions. The fixture provides a Swagger JSON file and a C# test file instead of a real codebase, so be lenient on project discovery (solution scanning, controller search) and focus on the quality of the derived documentation.

Score each dimension from 1 (poor) to 10 (excellent).

## Dimensions

### 1. Swagger Coverage
Whether all endpoints from the OpenAPI spec are documented in the ACCEPTANCE_CRITERIA.md API Surface section.

- 10 = Every endpoint from the fixture swagger.json is listed (GET/POST /rooms, GET/DELETE /rooms/{id}, GET/POST /bookings, DELETE /bookings/{id}) with correct HTTP methods, paths, and summaries
- 5 = Most endpoints listed but one or two are missing or have incorrect summaries
- 1 = Fewer than half the endpoints are documented, or endpoints are fabricated that don't exist in the spec

### 2. Test-Derived Requirements
Whether functional requirements are correctly inferred from the unit test file, capturing the behaviours being tested.

- 10 = Requirements reflect all tested behaviours: room CRUD, duplicate name rejection, floor filtering, delete-with-bookings conflict, booking creation, time slot conflicts, past booking cancellation, date range filtering
- 5 = Most tested behaviours captured but one or two are missed
- 1 = Requirements don't reflect the tests; are generic or hallucinated

### 3. Milestone Zero Quality
Whether Milestone 0 correctly summarises the current state as a baseline audit with appropriate sections.

- 10 = Milestone 0 includes: what exists (endpoint count, test count, Swagger presence), API surface summary, test coverage summary, known gaps, and all done-when criteria are checked off
- 5 = Milestone 0 is present but missing one or two of the required sub-sections
- 1 = No Milestone 0, or it's a generic placeholder rather than a meaningful audit summary

### 4. Coverage Gap Identification
Whether the output identifies areas that are untested or undocumented based on comparing the Swagger spec against the test file.

- 10 = Gaps are specific and accurate (e.g. "no tests for GET /rooms/{id}", "no tests for GET /bookings date range validation", "no tests for 404 responses on room endpoints"); each gap is actionable
- 5 = Some gaps identified but they're vague or miss obvious ones
- 1 = No coverage gaps section, or gaps are generic ("needs more testing")

### 5. Content Accuracy
Whether all documented requirements, endpoints, and test summaries are faithful to the fixture data with no hallucination.

- 10 = Every fact in both output files traces back to the swagger.json or tests.cs fixtures; no invented endpoints, test names, or behaviours
- 5 = Mostly accurate but one or two details are embellished or slightly wrong
- 1 = Significant hallucination — endpoints, tests, or behaviours that don't exist in the fixtures

### 6. Structure Compliance
Whether both output files follow the templates specified in the skill file.

- 10 = ACCEPTANCE_CRITERIA.md has all required sections (Overview, Target User, Tech Stack, API Surface, Functional Requirements, Non-Functional Requirements, Coverage Gaps); MILESTONES.md has Tech Stack header and Milestone 0 with all sub-sections
- 5 = Most sections present but one or two are missing or misplaced
- 1 = Output does not follow either template; major sections missing

### 7. Conciseness
Whether the output is appropriately tight — requirements are focused, API surface is tabular, no filler.

- 10 = Requirements are one-line statements; API surface is a clean list; no meta-commentary about the audit process or fixture limitations
- 5 = Mostly concise but some sections are verbose or include unnecessary detail
- 1 = Verbose, repetitive, or includes significant meta-commentary

## Output Format

Respond with ONLY a JSON object, no other text:

```json
{
  "swagger_coverage": { "score": 0, "reasoning": "" },
  "test_derived_requirements": { "score": 0, "reasoning": "" },
  "milestone_zero_quality": { "score": 0, "reasoning": "" },
  "coverage_gap_identification": { "score": 0, "reasoning": "" },
  "content_accuracy": { "score": 0, "reasoning": "" },
  "structure_compliance": { "score": 0, "reasoning": "" },
  "conciseness": { "score": 0, "reasoning": "" },
  "total": 0,
  "max_possible": 70,
  "suggestions": []
}
```
