You are generating a `FEATURE.md` document for the current project by combining information from `MILESTONES.md` and `ACCEPTANCE_CRITERIA.md`.

---

## Step 1 — Read the source files

Read both `ACCEPTANCE_CRITERIA.md` and `MILESTONES.md` from the project root. If either file is missing, tell the user and stop — this skill requires both files to exist. Suggest they run `/invest-idea` first.

---

## Step 2 — Extract what you can

From the files, extract:

| FEATURE.md section | Source |
|---|---|
| Title | First heading in ACCEPTANCE_CRITERIA.md or infer from Overview |
| As a / I want / So that | Target User + Overview in ACCEPTANCE_CRITERIA.md |
| Context | Overview section |
| Requirements Specification body | Functional Requirements + Non-Functional Requirements |
| Functional Specification body | All milestones summarised as a development plan |
| Definition of Done | "Done when" criteria from the final milestone(s) |
| Out of Scope (Risks) | Out of Scope section, if present |

Also derive these two fields as best you can from the source files:

**KPIs** — infer measurable success metrics from the Functional Requirements and Non-Functional Requirements. For example: if the spec mentions response times, uptime, user actions, or conversion goals, turn those into KPI statements. If nothing can be inferred, note that they could not be derived.

**Test Requirements** — compile every "Done when" criterion from all milestones into a checklist. Supplement with any testable Functional Requirements from ACCEPTANCE_CRITERIA.md that are not already covered.

Do not invent content not present in the source files. Where something is clearly not covered, leave a placeholder.

---

## Step 3 — Collect human-only fields

Ask the user for information that cannot be derived from the files, **one question at a time**, in order. Skip any question whose answer is already clear from context.

For **KPIs** and **Test Requirements**, show the user what you derived in Step 2 before asking, then ask if they are happy with it or want to add/change anything. Only replace the derived content if the user provides new content — otherwise keep what was derived.

1. **Written by (Hypothesis):** Who wrote the hypothesis? (name or role)
2. **Written by (Requirements Specification):** Who is the PM?
3. **Approved by (Requirements Specification):** Who is the approving stakeholder?
4. **KPIs:** Show the derived KPIs and ask: "Are you happy with these KPIs, or would you like to add or change anything?"
5. **Existing Functionality:** What does this replace or build on, if anything?
6. **Written by (Functional Specification):** Which developer(s) will write the functional spec?
7. **Approved by (Functional Specification):** Who approves it (stakeholder and PM/Head of Development)?
8. **Risks:** What are the key risks?
9. **Written by (Test Requirements):** Who writes the test requirements?
10. **Approved by (Test Requirements):** Who approves them?
11. **Tested by:** Who will perform testing?
12. **Test Requirements:** Show the derived test requirements checklist and ask: "Are you happy with these test requirements, or would you like to add or change anything?"

---

## Step 4 — Write FEATURE.md

Create `FEATURE.md` in the project root using the structure below, filled with extracted and collected values.

```
# [Title]


# Hypothesis

> 👥 Written by: [answer 1]

## 🧑‍💼 As a:

[Target user from ACCEPTANCE_CRITERIA.md]

## 🎯 I want:

[High-level need from Overview]

## 💡 So that:

[Why — inferred from Overview]

## ✨ Context

[Overview from ACCEPTANCE_CRITERIA.md]

---

# Requirements Specification

> 👥 Written by: [answer 2]
>
> Approved by: [answer 3]

[Functional Requirements and Non-Functional Requirements from ACCEPTANCE_CRITERIA.md]

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

[Milestones summarised as a development plan — each milestone as a paragraph or sub-section]

## Definition of Done

[Done when criteria from the final milestone(s)]

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

After writing the file, copy its contents to the clipboard so the user can paste them straight into another tool (ticket tracker, Slack, Notion, etc.) without reopening the file:

```bash
cat FEATURE.md | python ~/.claude/scripts/copy_to_clipboard.py
```

If the clipboard command exits non-zero, print its stderr and note that the clipboard copy failed — but the file is still saved and is the source of truth.

Tell the user where the file was saved, that the full contents are now on the clipboard (also available via Win+V history on Windows if clipboard history is enabled), and what sections may still need manual updates (e.g. designs, detailed functional spec prose).
