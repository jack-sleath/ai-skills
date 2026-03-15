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

Before writing, ask the user the following questions **one at a time** to collect information that cannot be derived automatically. Skip any question whose answer is already clear from context.

For **KPIs**, derive measurable success metrics from the new Functional and Non-Functional Requirements (e.g. response times, conversion goals, error rates). Show the user what you derived and ask if they are happy with it or want to add or change anything.

For **Test Requirements**, compile every "Done when" criterion from the new milestones into a checklist. Supplement with any testable Functional Requirements from the new change section that are not already covered. Show the user and ask if they are happy with it or want to change anything.

1. **Written by (Hypothesis):** Who wrote the hypothesis for this change? (name or role)
2. **Written by (Requirements Specification):** Who is the PM?
3. **Approved by (Requirements Specification):** Who is the approving stakeholder?
4. **KPIs:** Show derived KPIs and ask: "Are you happy with these KPIs, or would you like to add or change anything?"
5. **Existing Functionality:** What does this change replace or build on, if anything?
6. **Written by (Functional Specification):** Which developer(s) will write the functional spec?
7. **Approved by (Functional Specification):** Who approves it?
8. **Risks:** What are the key risks for this change?
9. **Written by (Test Requirements):** Who writes the test requirements?
10. **Approved by (Test Requirements):** Who approves them?
11. **Tested by:** Who will perform testing?
12. **Test Requirements:** Show the derived test requirements checklist and ask: "Are you happy with these, or would you like to add or change anything?"

Then write `<CHANGE-TITLE>_FEATURE.md` in the project root using this structure:

```
# [Change Request Title]


# Hypothesis

> 👥 Written by: [answer 1]

## 🧑‍💼 As a:

[Target user / who raised this feedback]

## 🎯 I want:

[High-level need from the change request Overview]

## 💡 So that:

[Why — inferred from Overview and the problem being solved]

## ✨ Context

[Overview from the new ACCEPTANCE_CRITERIA section]

---

# Requirements Specification

> 👥 Written by: [answer 2]
>
> Approved by: [answer 3]

[Functional Requirements and Non-Functional Requirements from the new change section]

## KPIs

[Derived KPIs, updated with any user input from answer 4]

## Existing Functionality

[answer 5]

---

# Functional Specification

> 👥 Specification
>
> Written by: [answer 6]
>
> Approved by: [answer 7]

[New milestones summarised as a development plan — each milestone as a paragraph or sub-section]

## Definition of Done

[Done when criteria from the final new milestone(s)]

---

# Risks

- [answer 8]

---

# Test Requirements

> 👥 Written by: [answer 9]
>
> Approved by: [answer 10]
>
> Tested by: [answer 11]

[Derived test requirements checklist, updated with any user input from answer 12]

## Test Results

> [To be completed after testing phase. Include pass/fail status for each of the above requirements.]
```

---

After creating all three outputs, summarise what was produced and suggest the user run:
- `/milestone` to begin implementing the new milestones
- `/ship` to implement all new milestones in sequence and raise PRs
