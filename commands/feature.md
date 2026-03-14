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
| Test Requirements checklist | "Done when" criteria from all milestones, formatted as checkboxes |
| Out of Scope (Risks) | Out of Scope section, if present |

Do not invent content not present in the source files. Where something is clearly not covered, leave a placeholder.

---

## Step 3 — Collect human-only fields

Ask the user for information that cannot be derived from the files, **one question at a time**, in order. Skip any question whose answer is already clear from context.

1. **Written by (Hypothesis):** Who wrote the hypothesis? (name or role)
2. **Written by (Requirements Specification):** Who is the PM?
3. **Approved by (Requirements Specification):** Who is the approving stakeholder?
4. **KPIs:** What metrics will measure success?
5. **Existing Functionality:** What does this replace or build on, if anything?
6. **Written by (Functional Specification):** Which developer(s) will write the functional spec?
7. **Approved by (Functional Specification):** Who approves it (stakeholder and PM/Head of Development)?
8. **Risks:** What are the key risks?
9. **Written by (Test Requirements):** Who writes the test requirements?
10. **Approved by (Test Requirements):** Who approves them?
11. **Tested by:** Who will perform testing?

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

- [answer 4]

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

[Done when criteria from all milestones as checkboxes]

## Test Results

> [To be completed after testing phase. Include pass/fail status for each of the above requirements.]
```

---

After writing the file, tell the user where it was saved and what sections may still need manual updates (e.g. designs, detailed functional spec prose).
