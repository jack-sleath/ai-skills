# /feature Evaluation Criteria

You are scoring the output of the `/feature` skill. The skill reads `ACCEPTANCE_CRITERIA.md` and `MILESTONES.md` and produces a `FEATURE.md` document.

For this evaluation, the skill was run in **non-interactive mode** — it could not ask the user follow-up questions, so human-only fields (Written by, Approved by, Tested by, etc.) should contain sensible placeholders.

Score each dimension from 1 (poor) to 5 (excellent).

## Dimensions

### 1. Structure Compliance
Does the output follow the exact FEATURE.md template defined in the skill (Hypothesis → Requirements Specification → Functional Specification → Risks → Test Requirements)?

- 5 = Every section and sub-section present in the correct order
- 3 = Most sections present, minor ordering or naming issues
- 1 = Major sections missing or wrong structure

### 2. Content Accuracy
Is the extracted content faithful to the source files? No hallucinated requirements, no missing functional/non-functional requirements.

- 5 = All source content accurately represented, nothing invented
- 3 = Mostly accurate with minor omissions or embellishments
- 1 = Significant hallucinated or missing content

### 3. KPI Derivation
Are the KPIs reasonable, measurable, and grounded in the source material (e.g. response time targets, rate limits)?

- 5 = KPIs are specific, measurable, and clearly tied to source requirements
- 3 = KPIs exist but are vague or partially grounded
- 1 = No KPIs or entirely invented metrics

### 4. Test Requirements Completeness
Does the test requirements section compile all "Done when" criteria from every milestone, plus any additional testable functional requirements?

- 5 = Every "Done when" item captured, supplemented with additional testable requirements
- 3 = Most criteria captured, some gaps
- 1 = Majority of test criteria missing

### 5. Placeholder Handling
For fields that require human input (Written by, Approved by, etc.), does the output use clear, consistent placeholders rather than inventing names?

- 5 = All human-only fields have clear placeholders (e.g. "[To be confirmed]")
- 3 = Some placeholders, some invented values
- 1 = Names or values invented wholesale

### 6. Conciseness
Is the document appropriately concise — no unnecessary repetition, no filler paragraphs, no over-elaboration beyond what the source provides?

- 5 = Tight, professional, no filler
- 3 = Some unnecessary elaboration but generally acceptable
- 1 = Bloated with filler or repetitive content

## Output Format

Respond with ONLY a JSON object, no other text:

```json
{
  "structure_compliance": { "score": <1-5>, "reasoning": "<one sentence>" },
  "content_accuracy": { "score": <1-5>, "reasoning": "<one sentence>" },
  "kpi_derivation": { "score": <1-5>, "reasoning": "<one sentence>" },
  "test_requirements_completeness": { "score": <1-5>, "reasoning": "<one sentence>" },
  "placeholder_handling": { "score": <1-5>, "reasoning": "<one sentence>" },
  "conciseness": { "score": <1-5>, "reasoning": "<one sentence>" },
  "total": <sum of all scores>,
  "max_possible": 30,
  "suggestions": ["<improvement 1>", "<improvement 2>"]
}
```
