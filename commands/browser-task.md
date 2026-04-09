You are generating a prompt for the Claude web/browser extension. Follow these phases in order.

## Phase 1 — Understand the Task

Ask clarifying questions **one at a time** (multiple choice + "Other") until you know:
- What needs doing in the browser?
- Target URL?
- What does success look like?
- Credentials needed? (Note what the user must supply — don't embed secrets.)

Skip questions already answered. Then read relevant project files (test output, source, config, criteria), summarise findings, and confirm with the user before proceeding.

## Phase 2 — Generate the Prompt

Output a single fenced markdown block. Rules for steps:
- Full URLs; no click-through chains.
- Name exact elements (selector, label, region) — never "scan the page".
- Batch same-page checks; order to minimise navigation.
- Embed exact expected values inline.

```markdown
# Browser Task

## What to Do
<Numbered steps. Each: exact element/selector + full URL. Same-page checks combined. Ordered to minimise navigation.>

## Context
<Expected values, known issues, auth state not already in steps.>

## Success Criteria
<Concrete checkable conditions with exact thresholds.>

## Output

Produce a downloadable file named `browser-result.md`:

\```markdown
---
task: "<title>"
status: "<pass | fail | partial | blocked>"
timestamp: "<ISO 8601>"
---
## Summary
<What was done and outcome>
## Steps Performed
<Numbered actions and results>
## Result
<Confirmations and values>
## Issues
<Blockers or "None">
\```
```

## Phase 3 — Handoff

Tell the user: paste the prompt into the Claude web extension, download `browser-result.md` when done, then share it here to continue.
