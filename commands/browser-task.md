You are generating a prompt that the user will paste into the Claude web/browser extension to perform a task that requires browser interaction. Follow these steps in order.

---

## Phase 1 — Understand the Task

Ask the user clarifying questions **one at a time** (multiple choice, with a final "Other — let me specify" option) to understand:

- What needs to be done in the browser? (e.g. fill a form, test a UI flow, verify a deployment, check a dashboard, scrape information, interact with a third-party service)
- What is the target URL or starting point?
- What does success look like — what information or confirmation should come back?
- Are there any credentials, tokens, or context the browser Claude will need? (Do NOT include secrets in the prompt — just note what the user will need to provide manually.)

Ask **one question at a time**. Skip questions already answered by context.

---

## Phase 2 — Gather Local Context

Before generating the prompt, gather any relevant context from the current project that the browser Claude will need:

- If the task relates to test results, read the relevant test output or test files.
- If the task relates to a deployment or feature, read the relevant source files or config.
- If there are acceptance criteria or milestones that define what needs verifying, read those.

Summarise what you found — the user should confirm this context is correct before you generate the prompt.

---

## Phase 3 — Generate the Prompt

Output a single fenced code block (```markdown ... ```) containing the full prompt the user should paste into the Claude web extension. The prompt must follow this structure:

```markdown
# Browser Task

## What to Do
<Clear, step-by-step instructions for what the browser Claude should do>

## Context
<Relevant context gathered from the local project — test results, acceptance criteria, expected values, etc.>

## Success Criteria
<How to know the task is complete — what to verify, what values to check, what screenshots to take>

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
3. Come back here and share the file — e.g. by dragging it in or pasting its path — so we can continue where we left off.
