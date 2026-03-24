# /browser-task Evaluation Criteria

You are scoring the output of the `/browser-task` skill. This skill generates a prompt that the user will paste into the Claude web/browser extension to perform a task that requires browser interaction. The output is a structured markdown prompt with steps, context, success criteria, and an output template.

For this evaluation, the skill was run in **non-interactive mode** — it could not ask the user follow-up questions. The fixture provides a complete task description with URL, details, and expected values, so the skill should have had sufficient input to produce a full browser prompt.

Score each dimension from 1 (poor) to 10 (excellent).

## Dimensions

### 1. Step Specificity
Whether each step in the "What to Do" section specifies exactly what to look for and where — selectors, label text, page regions — rather than vague instructions.

- 10 = Every step names the exact element, label, heading, or selector to target (e.g. "check the element with text 'Last synced' in the top-right corner"); no "scan the page" or "look around"
- 5 = Most steps are specific but one or two use vague language like "check the dashboard" without targeting a specific element
- 1 = Steps are vague throughout ("verify the page looks correct", "check everything works")

### 2. Navigation Efficiency
Whether steps minimise page transitions and use direct URLs rather than click-through navigation.

- 10 = Uses direct URL navigation; all checks on the same page are batched into one step; steps are ordered to avoid back-and-forth between pages
- 5 = Mostly efficient but one unnecessary page transition or a check that could be batched is separated
- 1 = Steps bounce between pages, use click-through navigation when URLs would work, or re-read pages already captured

### 3. Expected Values Inclusion
Whether the prompt includes concrete expected values, strings, or patterns for the browser to match against.

- 10 = All expected values from the fixture are embedded in the prompt: page title "Inventory Dashboard — Staging", product categories, version "v2.4.1", chart selector "#analytics-chart canvas"
- 5 = Most expected values included but one or two are missing or vague
- 1 = No expected values provided; browser would need to interpret content without targets

### 4. Output Template Compliance
Whether the prompt includes the specified output format with frontmatter (task, status, timestamp), Summary, Steps Performed, Result, and Issues sections.

- 10 = Output section contains the exact template structure with YAML frontmatter and all four sections; uses downloadable file instruction for `browser-result.md`
- 5 = Output template mostly present but missing one section or the frontmatter
- 1 = No output template, or template is significantly different from the specification

### 5. Structure Compliance
Whether the overall prompt follows the specified structure: What to Do, Context, Success Criteria, Output.

- 10 = All four top-level sections present with correct headings; prompt is in a fenced markdown code block ready to paste
- 5 = Most sections present but one is missing or headings don't match the spec
- 1 = Prompt structure is unrecognisable or missing multiple sections

### 6. Conciseness
Whether the prompt is focused and efficient — no redundant reads, no verbose explanations, no filler.

- 10 = Each step is one clear instruction; context section provides only what's needed; no meta-commentary about how the browser works
- 5 = Mostly concise but some steps are verbose or context includes unnecessary detail
- 1 = Prompt is bloated with explanations, redundant checks, or meta-instructions

## Output Format

Respond with ONLY a JSON object, no other text:

```json
{
  "step_specificity": { "score": 0, "reasoning": "" },
  "navigation_efficiency": { "score": 0, "reasoning": "" },
  "expected_values_inclusion": { "score": 0, "reasoning": "" },
  "output_template_compliance": { "score": 0, "reasoning": "" },
  "structure_compliance": { "score": 0, "reasoning": "" },
  "conciseness": { "score": 0, "reasoning": "" },
  "total": 0,
  "max_possible": 60,
  "suggestions": []
}
```
