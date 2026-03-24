# /browser-task Evaluation Criteria

You are scoring the output of the `/browser-task` skill. This skill generates a prompt that the user will paste into the Claude web/browser extension to perform a task requiring browser interaction. The output is a single fenced code block containing a structured Markdown prompt with sections for What to Do, Context, Success Criteria, and Output.

For this evaluation, the skill was run in **non-interactive mode** — it could not ask the user clarifying questions about the task, so the task description was provided directly. Be lenient on any missing details that would normally come from interactive Q&A, but strict on the quality and structure of the generated prompt.

Score each dimension from 1 (poor) to 5 (excellent).

## Dimensions

### 1. Structure Compliance
Does the output follow the exact template: a fenced code block containing `# Browser Task` with `## What to Do`, `## Context`, `## Success Criteria`, and `## Output` sections (including the downloadable file template)?

- 5 = All sections present in correct order inside a fenced code block; Output section includes the `browser-result.md` template with frontmatter
- 3 = Most sections present but one missing or out of order, or not wrapped in a fenced code block
- 1 = Template not followed; output is freeform or missing multiple required sections

### 2. Step Specificity
Are the "What to Do" steps precise — targeting exact elements, labels, URLs, or page regions rather than vague instructions like "look around"?

- 5 = Every step names the exact element/label/URL/selector to target; uses direct URL navigation; no vague "scan the page" instructions
- 3 = Most steps are specific but one or two resort to vague targeting (e.g. "find the relevant section")
- 1 = Steps are mostly vague, requiring the browser to interpret or scan broadly

### 3. Navigation Efficiency
Are steps ordered to minimise page transitions, batch same-page checks, and avoid redundant page reads?

- 5 = All checks on the same page are batched into one step; no back-and-forth between pages; direct URLs used throughout
- 3 = Mostly efficient but one unnecessary page transition or unbatched same-page checks
- 1 = Steps bounce between pages, re-read already-captured content, or navigate via menus instead of direct URLs

### 4. Content Accuracy
Is the context section faithful to the provided fixture input, with no hallucinated URLs, values, or requirements?

- 5 = All context traces to the fixture input; expected values and patterns are accurate; no invented details
- 3 = Mostly faithful but includes one or two assumed details not in the input
- 1 = Multiple fabricated URLs, values, or requirements

### 5. Success Criteria Clarity
Are success criteria expressed as concrete, checkable conditions rather than vague descriptions?

- 5 = Each criterion is a specific, observable condition (e.g. "element with text 'Active' visible in #status-bar"); no ambiguity
- 3 = Most criteria are concrete but one or two are vague (e.g. "page looks correct")
- 1 = Criteria are all vague or unmeasurable

### 6. Conciseness
Is the prompt tight and free of filler, while still giving the browser Claude everything it needs?

- 5 = No unnecessary preamble, no redundant instructions, every line adds distinct value
- 3 = Some filler or redundancy but mostly on-point
- 1 = Verbose, repetitive, or padded with unnecessary explanation

## Output Format

Respond with ONLY a JSON object, no other text:

```json
{
  "structure_compliance": { "score": 1, "reasoning": "" },
  "step_specificity": { "score": 1, "reasoning": "" },
  "navigation_efficiency": { "score": 1, "reasoning": "" },
  "content_accuracy": { "score": 1, "reasoning": "" },
  "success_criteria_clarity": { "score": 1, "reasoning": "" },
  "conciseness": { "score": 1, "reasoning": "" },
  "total": 6,
  "max_possible": 30,
  "suggestions": []
}
```
