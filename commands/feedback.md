You are helping the user translate feedback or a change request into a concrete plan that extends an existing project. Follow these steps in order.

---

## Phase 1 — Understand the Change Request

The user has raised some feedback or a change request. Your job is to ask clarifying questions **one at a time** to build a full understanding of what needs to change and why.

**Question format:** Each question must be multiple choice. Always include a final option: "Other — let me specify".

Ask questions across these dimensions (adapt based on what you already know — skip questions that are already answered):
- What type of change is this? (new feature, enhancement to existing feature, bug fix, performance improvement, UX/design change, other)
- What is the core problem or need driving this change?
- Who raised this feedback? (end user, internal stakeholder, developer, QA, other)
- Which parts of the existing system does this change affect?
- What does success look like — how will you know the change is done and working?
- Are there any constraints or things that must not change?
- What is the MVP scope — the minimum needed to satisfy the feedback?

Ask **one question at a time**. Wait for the user's answer before asking the next. Do not ask a question if the answer is already clear from context.

When you have enough to describe the change clearly and completely, ask the user:

> **What should this change request be called?** This short title will be used in file and branch names (e.g. "dark-mode", "checkout-fix", "export-csv"). It should be lowercase with hyphens, no spaces.

Wait for the user to confirm the title before moving to Phase 2.

---

## Phase 2 — Read Existing Files

Read `ACCEPTANCE_CRITERIA.md` and `MILESTONES.md` from the project root.

If either file is missing, stop and tell the user — this skill requires both files to exist. Suggest they run `/invest-idea` first to set up the project.

From `MILESTONES.md`, find the highest milestone number present (e.g. if the last milestone is "Milestone 4", the next will be Milestone 5). Remember this number.

---

## Phase 3 — Generate Output Files

Using everything gathered, produce the following three outputs.

### Output 1: Append to `ACCEPTANCE_CRITERIA.md`

At the bottom of the existing file, append a new section for this change request:

```
---

## Change Request — <change-title>

### Overview
<1–2 sentence description of what this change adds or fixes and why>

### Raised By
<who raised this feedback>

### Functional Requirements
A numbered list of "The system must..." or "The user can..." statements covering the agreed scope of this change.

### Non-Functional Requirements
Any quality attributes specific to this change (performance, security, accessibility, etc.). Only include ones discussed or clearly implied.

### Out of Scope
Anything explicitly excluded or deferred for this change request.
```

### Output 2: Append to `MILESTONES.md`

At the bottom of the existing file, append new milestones continuing the numbering from where the file left off. Use this structure for each new milestone:

```
---

## Milestone N — <name> [<change-title>]
**Branch:** milestone-N-<change-title>
**Goal:** <one sentence>

**Tasks:**
- ...

**Done when:**
- [ ] <concrete, verifiable criterion>
- [ ] <concrete, verifiable criterion>
```

**Milestone guidelines:**
- Tag each milestone heading with `[<change-title>]` so it is clearly associated with this change request.
- Each milestone should be independently deployable or testable where possible.
- The first new milestone should lay the groundwork for the change (e.g. data model changes, new routes, UI scaffolding).
- Later milestones build up the change incrementally, each with clear "Done when" criteria that map back to the new Functional Requirements.
- The final new milestone should result in a state that satisfies all new Functional Requirements for this change.
- Keep milestones small enough to be completable in a focused work session.

### Output 3: Create `<CHANGE-TITLE>_FEATURE.md`

Generate this file by following the `/feature` skill, with these differences:

- Source content **only** from the new change request section appended to `ACCEPTANCE_CRITERIA.md` in Output 1 (not the full file).
- Use **only** the new milestones appended to `MILESTONES.md` in Output 2 (not all milestones).
- Name the output file `<CHANGE-TITLE>_FEATURE.md` (e.g. `dark-mode_FEATURE.md`) instead of `FEATURE.md`.

---

After creating all three outputs, summarise what was produced and suggest the user run:
- `/milestone` to begin implementing the new milestones
- `/ship` to implement all new milestones in sequence and raise PRs
