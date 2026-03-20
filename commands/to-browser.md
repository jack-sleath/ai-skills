You are converting instructions that were just given in this conversation into a prompt for the Claude web/browser extension.

---

## Phase 1 — Extract Instructions

Look back through the current conversation and identify the most recent set of instructions, manual steps, or browser-based actions that were given to the user. These are typically things Claude terminal cannot do itself — e.g. "go to this URL", "click this button", "check this dashboard", "fill in this form", "verify this in the browser".

Summarise the extracted instructions and present them to the user for confirmation:

> **I found these instructions to hand off to the browser:**
> <numbered list of steps>
>
> Does this look right, or should I adjust anything?

Wait for the user to confirm before proceeding.

---

## Phase 2 — Gather Supporting Context

Scan the conversation and project for any context the browser Claude will need to complete the task:

- URLs, expected values, test data, or credentials references mentioned in the conversation.
- If the instructions reference test results, acceptance criteria, or source files — read those files and include the relevant parts.

---

## Phase 3 — Generate the Prompt

Output a single fenced code block (```markdown ... ```) containing the full prompt the user should paste into the Claude web extension. The prompt must follow this structure:

```markdown
# Browser Task

## What to Do
<Clear, step-by-step instructions extracted from the conversation>

## Context
<Relevant context from the conversation and local project — test results, expected values, configuration, etc.>

## Success Criteria
<How to know the task is complete — what to verify, what values to check>

## Output

When you are finished, produce a single Markdown file with the following structure and offer it as a **downloadable file** named `browser-result.md`:

\```markdown
---
task: "<short task title>"
status: "<pass | fail | partial | blocked>"
timestamp: "<ISO 8601 timestamp>"
---

## Summary
<1–3 sentence summary of what was done and the outcome>

## Steps Performed
<Numbered list of each action taken, with the result of each step>

## Result
<The information or confirmation requested, including any values, screenshots described, or data gathered>

## Issues
<Any problems encountered, unexpected behaviour, or blockers. Write "None" if everything went smoothly.>
\```
```

---

## Phase 4 — Handoff

After presenting the prompt, tell the user:

1. Copy the prompt above and paste it into the Claude web extension.
2. When the browser task is done, download the `browser-result.md` file.
3. Come back here and share the file so we can continue where we left off.
