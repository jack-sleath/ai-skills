# /story Evaluation Criteria

You are scoring the output of the `/story` skill. This skill takes a product or technical specification and generates a story card with a title, original spec in a collapsible section, technical notes, and GIVEN/WHEN/THEN acceptance criteria.

For this evaluation, the skill was run in **non-interactive mode** — the specification was provided directly as fixture input, so no follow-up questions were needed.

Score each dimension from 1 (poor) to 5 (excellent).

## Dimensions

### 1. Structure Compliance
Does the output follow the exact template: Title, collapsible Original Spec, Technical Notes, then GIVEN/WHEN/THEN blocks?

- 5 = All sections present in the correct order; `<details>` tag used correctly for original spec
- 3 = Most sections present but one missing or out of order (e.g. no Technical Notes section)
- 1 = Template not followed; output is freeform or missing multiple required sections

### 2. Gherkin Syntax
Are the acceptance criteria written in correct GIVEN/WHEN/AND/THEN format with those keywords in bold capitals?

- 5 = All scenarios use **GIVEN**/**WHEN**/**AND**/**THEN** correctly, bolded and capitalised
- 3 = Keywords present but inconsistently bolded/capitalised, or AND used incorrectly
- 1 = No Gherkin format; criteria are plain bullet points or freeform text

### 3. Scenario Coverage
Do the acceptance criteria cover both positive (happy path) and negative (error/edge) cases?

- 5 = All major happy paths covered plus at least 2 distinct negative/edge cases
- 3 = Happy paths covered but only 1 or no negative cases
- 1 = Only one scenario, or major paths from the spec are missing entirely

### 4. Content Accuracy
Are the criteria faithful to the input specification, with no hallucinated requirements?

- 5 = Every scenario traces to something in the spec; no invented behaviour
- 3 = Mostly faithful but one or two scenarios add assumptions not in the spec
- 1 = Multiple scenarios describe behaviour not in the specification

### 5. Testability
Are the criteria specific enough that a tester could write a test from them without guessing?

- 5 = Each THEN clause describes a concrete, observable outcome (e.g. "returns 404", "displays error message X")
- 3 = Most outcomes are clear but some are vague (e.g. "behaves correctly", "handles it")
- 1 = Outcomes are all vague or unmeasurable

### 6. Conciseness
Is the output tight without redundant or filler scenarios?

- 5 = No duplicate scenarios, no unnecessary preamble, each block adds distinct value
- 3 = Some redundancy between scenarios or minor filler text
- 1 = Multiple scenarios test the same thing, or output is padded with unnecessary explanation

## Output Format

Respond with ONLY a JSON object, no other text:

```json
{
  "structure_compliance": { "score": 1, "reasoning": "" },
  "gherkin_syntax": { "score": 1, "reasoning": "" },
  "scenario_coverage": { "score": 1, "reasoning": "" },
  "content_accuracy": { "score": 1, "reasoning": "" },
  "testability": { "score": 1, "reasoning": "" },
  "conciseness": { "score": 1, "reasoning": "" },
  "total": 6,
  "max_possible": 30,
  "suggestions": []
}
```
