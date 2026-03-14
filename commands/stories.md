You are generating story cards for every milestone in this project's `MILESTONES.md` file.

---

## Step 1 — Read MILESTONES.md

Read `MILESTONES.md` from the project root. If it is missing, tell the user and stop — suggest they run `/invest-idea` first.

---

## Step 2 — Generate a story card per milestone

For each milestone in the file, apply the following story card format. Treat the milestone's name, goal, tasks, and "Done when" criteria as the specification.

Produce exactly this structure for each milestone:

```
---

Title: <short descriptive title based on the milestone name>

<details>
<summary>Original Spec</summary>

**Goal:** <milestone goal>

**Tasks:**
<task list>

**Done when:**
<done when criteria>

</details>


Technical Notes:
<implementation details inferred from the milestone — note any backend-only behaviour, infrastructure steps, or scaffolding. Write "None" if not applicable>


**GIVEN** ...
**WHEN** ...
**AND** ...
**THEN** ...

**GIVEN** ...
**WHEN** ...
**AND** ...
**THEN** ...
```

---

## Rules

- Write acceptance criteria from the end-user perspective where possible. For infrastructure or backend-only milestones, state this clearly in Technical Notes and write criteria from a developer/operator perspective instead.
- Use **BOLD CAPITALISED** GIVEN / WHEN / AND / THEN
- Cover both positive and negative paths for each milestone
- Do not invent requirements beyond what the milestone specifies
- Keep language precise, explicit, and testable
- If anything is unclear, undefined, or assumed — mark it **BOLD CAPITALISED** and flag for **MANUAL REVIEW**
- Separate each milestone's story card with a horizontal rule (`---`)

---

## Step 3 — Write files

Create a `stories/` folder in the project root if it does not already exist.

For each milestone, write its story card to a file named `milestone-N.md` (e.g. `stories/milestone-1.md`, `stories/milestone-2.md`) where N matches the milestone number.

Each file should contain only that milestone's story card content — no separating `---` between files.

After all files are written, tell the user how many story cards were created and list the file paths. Suggest they run `/story` for any individual piece of work that needs its own card.
