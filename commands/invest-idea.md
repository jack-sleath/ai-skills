You are helping the user flesh out a software idea into a concrete, actionable plan. Follow these steps in order.

---

## Phase 1 — Understand the Idea

The user has provided a concept with minimal information. Your job is to ask clarifying questions **one at a time** to build a full understanding of the idea.

**Question format:** Each question must be multiple choice. Always include a final option: "Other — let me specify".

Ask questions across these dimensions (but adapt based on what you already know — skip questions that are already answered):
- What is the core purpose / problem being solved?
- Who is the target user?
- Is this a web app, mobile app, CLI tool, API/service, library, desktop app, or something else?
- What is the primary interaction model? (e.g. user interface, automated/background, API consumed by other systems)
- What is the rough scale? (personal/hobby project, small team internal tool, production SaaS, open source library, etc.)
- What data does it store or process, if any?
- Does it need user authentication?
- Does it integrate with any external services or APIs?
- What are the most important features for an MVP?

Ask **one question at a time**. Wait for the user's answer before asking the next. Do not ask a question if the answer is already clear from context.

When you have enough to describe the idea clearly and completely, move to Phase 2.

---

## Phase 2 — Language and Framework Preferences

Now ask about technical preferences, again **one question at a time**, multiple choice with "Other — let me specify" as the last option.

Ask about:
- Preferred programming language(s)
- Preferred framework(s) relevant to the type of project (e.g. for web: React/Vue/Angular/HTMX; for backend: Express/FastAPI/Rails/ASP.NET; for mobile: React Native/Flutter/Swift/Kotlin; etc.)
- Preferred database or data store, if applicable
- Any infrastructure or hosting preferences (e.g. serverless, Docker/containers, specific cloud provider)
- Any hard constraints (e.g. must be open source, must run offline, must use company's existing stack)

When you have clear answers (or the user has said they have no preference for remaining questions), move to Phase 3.

---

## Phase 3 — Generate Output Files

Using everything gathered, create two files in the project root.

### File 1: `ACCEPTANCE_CRITERIA.md`

Structure:
```
# Acceptance Criteria

## Overview
<1–2 sentence description of what the finished product is and does>

## Target User
<who this is for>

## Tech Stack
- Language: ...
- Framework(s): ...
- Database: ...
- Hosting/Infrastructure: ...

## Functional Requirements
A numbered list of "The system must..." or "The user can..." statements covering all agreed features.

## Non-Functional Requirements
Quality attributes: performance, security, accessibility, offline support, etc. Only include ones that were discussed or are clearly implied.

## Out of Scope
Anything explicitly excluded or deferred.
```

### File 2: `FEATURE.md`

Use the title of the idea as the document title. Fill in as much as possible from the gathered information; leave placeholder text for anything that requires human input (e.g. stakeholder names, KPIs, designs).

Structure:
```
# [Title here]


# Hypothesis

> 👥 Written by:

## 🧑‍💼 As a:

[Enter main user persona]

## 🎯 I want:

[High level need]

## 💡 So that:

[Why?]

## ✨ Context

[Background context]

---

# Requirements Specification

> 👥 Written by: [PM]
>
> Approved by: [Stakeholder]

[Detailed high-level requirements]

## KPIs

- [What are we measuring]

## Existing Functionality

[What existing functionality is there? What are we replacing?]

---

# Functional Specification

> 👥 Specification
>
> Written by: [Developer/s] *(Scrum says this can be any software or product developer AND can in theory be written during sprint planning)*
>
> Approved by: [Stakeholder and PM/Head of Development]

[Detailed specification]

[Add designs when available]

## Definition of Done

[What will signify this piece of work being complete - agreed by all Developers]

---

# Risks

- [What risks might there be?]

---

# Test Requirements

> 👥 Written by: [PM with Developer and Stakeholder input]
>
> Approved by: [Stakeholder/Head of Development]
>
> Tested by: [Developer PM Stakeholder]

- [ ] What do we need to test to confirm success.

## Test Results

> [To be completed after testing phase. Include pass/fail status for each of the above requirements.]
```

---

### File 3: `MILESTONES.md`

Structure:
```
# Milestones

## Tech Stack
- Language: ...
- Framework(s): ...
- Database: ...
- Hosting/Infrastructure: ...

---

## Milestone 1 — <name>
**Goal:** <one sentence>

**Tasks:**
- ...

**Done when:**
- [ ] <concrete, verifiable criterion>
- [ ] <concrete, verifiable criterion>

---

## Milestone 2 — <name>
...
```

**Milestone guidelines:**
- Each milestone should be independently deployable or testable where possible.
- Milestone 1 should always be a working skeleton / project scaffold with the chosen stack configured and a trivial end-to-end path verified (e.g. "app starts and returns a health check response").
- Later milestones build up features incrementally, each with clear "Done when" criteria that map back to the Acceptance Criteria.
- The final milestone should result in a product that satisfies all Acceptance Criteria.
- Keep milestones small enough to be completable in a focused work session.

---

After creating all three files, summarise what was produced and suggest the user run `/milestone` to begin implementation.
