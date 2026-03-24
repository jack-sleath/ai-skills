# /feature Evaluation Criteria

You are scoring the output of the `/feature` skill. This skill generates a `FEATURE.md` document by combining information from `ACCEPTANCE_CRITERIA.md` and `MILESTONES.md`, producing a structured feature specification with hypothesis, requirements, functional specification, risks, and test requirements sections.

For this evaluation, the skill was run in **non-interactive mode** — it could not ask the user follow-up questions. Since the skill normally asks 12 questions to collect human-only fields (written by, approved by, KPIs, risks, etc.), be lenient on placeholder values for those fields. Focus on how well the skill extracts and organises content from the source files.

Score each dimension from 1 (poor) to 10 (excellent).

## Dimensions

### 1. Structure Compliance
Whether the output follows the exact FEATURE.md template structure specified in the skill file.

- 10 = All sections present in correct order: Hypothesis (As a/I want/So that/Context), Requirements Specification (with KPIs, Existing Functionality), Functional Specification (with Definition of Done), Risks, Test Requirements (with Test Results stub)
- 5 = Most sections present but one or two are missing or in the wrong order
- 1 = Output does not follow the template; major sections missing or structure is unrecognisable

### 2. Content Extraction Accuracy
Whether information is faithfully extracted from ACCEPTANCE_CRITERIA.md and MILESTONES.md without hallucination.

- 10 = All extracted content (overview, target user, functional requirements, milestones, done-when criteria) matches the source files exactly; no invented requirements or features
- 5 = Most content is accurate but one or two details are slightly altered or embellished beyond what the sources say
- 1 = Significant hallucination — requirements, features, or details that don't exist in the source files

### 3. Field Derivation Quality
Whether the skill correctly derives KPIs from requirements and compiles test requirements from done-when criteria.

- 10 = KPIs are logically inferred from non-functional requirements (e.g. response time targets, rate limits); test requirements checklist covers all done-when criteria from milestones plus testable functional requirements
- 5 = KPIs or test requirements are partially derived but miss obvious items from the source material
- 1 = No attempt to derive KPIs or test requirements; sections are empty or contain only placeholders

### 4. Milestone Summarisation
Whether the milestones from MILESTONES.md are accurately summarised as a development plan in the Functional Specification section.

- 10 = Each milestone is summarised as a coherent paragraph or sub-section capturing its goal, key tasks, and done-when criteria; nothing omitted or invented
- 5 = Milestones are listed but summaries are too brief or miss key details
- 1 = Milestones are omitted, copied verbatim without summarisation, or significantly misrepresented

### 5. Placeholder Handling
Whether human-only fields that cannot be derived are handled with clear placeholders rather than hallucinated values.

- 10 = All human-only fields (written by, approved by, tested by, risks, existing functionality) use clear placeholder text like "[To be provided]" — no fabricated names or roles
- 5 = Most placeholders are present but one or two fields have invented values
- 1 = Multiple human-only fields contain fabricated names, roles, or content

### 6. Conciseness
Whether the output is appropriately tight without filler, redundancy, or unnecessary commentary.

- 10 = Every section is focused and proportionate; no repeated information between sections; no meta-commentary about the generation process
- 5 = Mostly concise but some redundancy between sections or minor filler
- 1 = Verbose, repetitive, or includes significant meta-commentary about what the skill is doing

## Output Format

Respond with ONLY a JSON object, no other text:

```json
{
  "structure_compliance": { "score": 0, "reasoning": "" },
  "content_extraction_accuracy": { "score": 0, "reasoning": "" },
  "field_derivation_quality": { "score": 0, "reasoning": "" },
  "milestone_summarisation": { "score": 0, "reasoning": "" },
  "placeholder_handling": { "score": 0, "reasoning": "" },
  "conciseness": { "score": 0, "reasoning": "" },
  "total": 0,
  "max_possible": 60,
  "suggestions": []
}
```
