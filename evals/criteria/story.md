# /story Evaluation Criteria

You are scoring the output of the `/story` skill. This skill takes a product or technical specification and generates acceptance criteria in Gherkin-style format (GIVEN/WHEN/THEN), along with technical notes and open questions.

For this evaluation, the skill was run in **non-interactive mode** — it could not ask the user follow-up questions. The fixture provides a complete specification, so the skill should have had sufficient input to produce a full story card.

Score each dimension from 1 (poor) to 10 (excellent).

## Dimensions

### 1. Gherkin Syntax
Whether acceptance criteria use the correct GIVEN/WHEN/AND/THEN format with bold, capitalised keywords.

- 10 = Every scenario uses **GIVEN** / **WHEN** / **AND** / **THEN** (bold, capitalised) consistently; each scenario is 3–5 lines
- 5 = Keywords are present but inconsistently formatted (e.g. some not bold, mixed casing) or scenarios run long
- 1 = No Gherkin format used; criteria are written as prose or plain bullet points

### 2. Acceptance Criteria Coverage
Whether the scenarios cover all requirements from the specification, including both positive and negative paths.

- 10 = Every requirement from the spec has at least one scenario; both happy paths (successful reset, valid password) and negative paths (expired token, mismatched passwords, rate limiting, email enumeration prevention) are covered
- 5 = Most requirements covered but one or two are missing, or negative paths are underrepresented
- 1 = Fewer than half the requirements have scenarios, or only happy paths are covered

### 3. Testability
Whether each scenario is precise and testable — a QA engineer could execute it without ambiguity.

- 10 = Every scenario has specific, verifiable conditions and expected outcomes (e.g. exact error messages, specific behaviours, concrete values like "30 minutes" or "12 characters")
- 5 = Most scenarios are testable but a few have vague outcomes like "shows an error" without specifying what kind
- 1 = Scenarios are vague descriptions rather than testable conditions; outcomes are ambiguous

### 4. Content Accuracy
Whether the scenarios are faithful to the specification without inventing requirements or missing stated constraints.

- 10 = All scenarios trace directly to the spec; specific values (30 min expiry, 12 char minimum, 3 requests/hour rate limit, SHA-256 hashing) are correctly reflected; no invented requirements
- 5 = Mostly accurate but one or two details are slightly altered or a constraint is missed
- 1 = Contains scenarios for requirements not in the spec, or key constraints (rate limit, complexity rules) are wrong

### 5. Structure Compliance
Whether the output follows the specified template: Title, Original Spec in collapsible details, Technical Notes, Acceptance Criteria with numbered scenarios, Open Questions.

- 10 = All sections present in correct order; original spec is in a `<details>` collapsible; technical notes are one-line bullets; open questions flagged as **MANUAL REVIEW**
- 5 = Most sections present but one is missing or formatted incorrectly (e.g. spec not in collapsible)
- 1 = Output does not follow the template; sections missing or in wrong order

### 6. Technical Notes Accuracy
Whether backend-only details from the spec are correctly extracted into the Technical Notes section.

- 10 = All backend details (SHA-256 token hashing, Sidekiq job queue, session_version invalidation) appear as concise one-line bullets in Technical Notes
- 5 = Some backend details captured but one is missing or a frontend concern is incorrectly placed here
- 1 = No technical notes section, or it contains user-facing requirements instead of backend details

### 7. Conciseness
Whether the output is appropriately tight — scenarios are focused, notes are brief, no filler.

- 10 = Each scenario is 3–5 lines; technical notes are one sentence each; no meta-commentary or padding
- 5 = Mostly concise but some scenarios are verbose or notes are overly detailed
- 1 = Scenarios are paragraph-length; significant filler or meta-commentary throughout

## Output Format

Respond with ONLY a JSON object, no other text:

```json
{
  "gherkin_syntax": { "score": 0, "reasoning": "" },
  "acceptance_criteria_coverage": { "score": 0, "reasoning": "" },
  "testability": { "score": 0, "reasoning": "" },
  "content_accuracy": { "score": 0, "reasoning": "" },
  "structure_compliance": { "score": 0, "reasoning": "" },
  "technical_notes_accuracy": { "score": 0, "reasoning": "" },
  "conciseness": { "score": 0, "reasoning": "" },
  "total": 0,
  "max_possible": 70,
  "suggestions": []
}
```
