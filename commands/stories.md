You are generating story cards for every milestone in this project's `MILESTONES.md` file.

---

## Step 1 — Read MILESTONES.md

Read `MILESTONES.md` from the project root. If it is missing, tell the user and stop — suggest they run `/invest-idea` first.

---

## Step 2 — Generate a story card per milestone

For each milestone, treat its name, goal, tasks, and "Done when" criteria as the specification input and generate a story card using the same format, structure, and rules as the `/story` skill.

Separate each milestone's story card with a horizontal rule (`---`).

---

## Step 3 — Write files

Create a `stories/` folder in the project root if it does not already exist.

For each milestone, write its story card to a file named `milestone-N.md` (e.g. `stories/milestone-1.md`, `stories/milestone-2.md`) where N matches the milestone number.

Each file should contain only that milestone's story card content — no separating `---` between files.

After all files are written, tell the user how many story cards were created and list the file paths. Suggest they run `/story` for any individual piece of work that needs its own card.
