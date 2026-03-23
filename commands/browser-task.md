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

Output a single fenced code block (```markdown ... ```) containing the full prompt the user should paste into the Claude web extension.

**Optimisation rules** — apply these when writing the steps:

1. **Navigate directly.** Use full URLs instead of "go to the homepage, then click X, then click Y".
2. **Be specific about targets.** Name the exact element, label, heading, or page region to look at — never "scan the page" or "look around for".
3. **Batch same-page checks.** If multiple things need verifying on one page, combine them into a single step so the page is only read once.
4. **Minimise page transitions.** Order steps so all work on Page A is done before moving to Page B. Never bounce between pages.
5. **Provide expected values.** Give the exact strings, numbers, or patterns the browser should match against so it can do a targeted comparison instead of interpreting the full page content.
6. **Skip redundant reads.** Never ask the browser to re-read or re-screenshot a page it has already captured unless the page state has changed.

The prompt must follow this structure:

```markdown
# Browser Task

## What to Do
<Clear, step-by-step instructions for what the browser Claude should do.
 Each step should specify EXACTLY what to look for and where — e.g. a selector, label text, or page region — so the browser can target reads narrowly rather than scanning the full page.
 Prefer direct URL navigation over clicking through menus.
 Combine checks that are on the same page into a single step.
 Order steps to minimise back-and-forth navigation between pages.>

## Context
<Relevant context gathered from the local project — test results, acceptance criteria, expected values, etc.
 Include exact expected values, strings, or patterns so the browser can do targeted comparisons instead of reading and interpreting large blocks of content.>

## Success Criteria
<How to know the task is complete — what to verify, what values to check, what screenshots to take.
 Express each criterion as a concrete, checkable condition (e.g. "element with text 'Deployed' is visible in the #status banner") rather than a vague description.>

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
