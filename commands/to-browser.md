You are converting instructions that were just given in this conversation into a prompt for the Claude web/browser extension. This skill is a thin wrapper around `/browser-task` — extract the relevant context from the chat, confirm it, then delegate the prompt generation and clipboard handoff to `/browser-task`.

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

## Phase 3 — Delegate to /browser-task

Invoke `/browser-task` via the Skill tool. All of the clarifying-question items from `/browser-task` Phase 1 — what to do, target URL, success criteria, credentials — are already answered by Phases 1 and 2 above, so `/browser-task` **must skip its Phase 1 entirely**. Do not re-ask the user any of those questions, and do not re-read files you already consulted.

`/browser-task` owns the rest of the flow from here: generating the `# Browser Task` prompt, writing it to the temp file, copying it to the clipboard, and telling the user how to hand off to the Claude web extension. Do not duplicate any of that work in this skill.
