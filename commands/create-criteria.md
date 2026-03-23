You are scaffolding evaluation criteria and test fixtures for one or more skill commands, so they can be used with `/evolve`.

---

## Step 0 — Parse arguments

Check what the user passed:

- **One or more commands** — e.g. `/create-criteria commit` or `/create-criteria commit,story,audit`
- **No arguments** — list commands in `commands/` that do NOT yet have a file in `evals/criteria/` and ask the user to pick one or more.

Commands can be separated by commas or spaces.

---

## Step 1 — Check what already exists

For each command in the list:

1. Check if `commands/<command>.md` exists. If not, skip it with a warning.
2. Check if `evals/criteria/<command>.md` already exists. If so, note it as "already exists" — the user will be asked whether to overwrite.
3. Check if `evals/fixtures/<command>/` already exists and has files.

Show a summary:

```
┌─ Criteria Setup ─────────────────────────────┐
│ Command       Criteria     Fixtures           │
│ ─────────     ────────     ────────           │
│ commit        NEW          NEW                │
│ story         NEW          NEW                │
│ audit         EXISTS       NEW                │
│ fakecmd       ✗ no skill file — skipping      │
└───────────────────────────────────────────────┘
```

If any criteria files already exist, ask: **Overwrite existing criteria, or skip those commands?**

---

## Step 2 — Read each command's skill file

For each command being processed, read `commands/<command>.md` thoroughly. Identify:

1. **What the command does** — its purpose and expected output.
2. **What inputs it expects** — files it reads, arguments it takes, context it needs.
3. **What "good output" looks like** — structure, tone, completeness, accuracy.
4. **What could go wrong** — hallucination, missing sections, wrong format, verbosity.
5. **Whether it's interactive** — does it ask the user questions? (In eval mode it can't, so note this.)

---

## Step 3 — Generate criteria

For each command, create `evals/criteria/<command>.md` following this structure exactly:

```markdown
# /<command> Evaluation Criteria

You are scoring the output of the `/<command>` skill. <One sentence describing what the skill does and what output it produces>.

For this evaluation, the skill was run in **non-interactive mode** — it could not ask the user follow-up questions<, so add any relevant caveats about what the scorer should be lenient on>.

Score each dimension from 1 (poor) to 5 (excellent).

## Dimensions

### 1. <Dimension Name>
<What this dimension measures — one sentence>

- 5 = <specific definition of excellent>
- 3 = <specific definition of acceptable>
- 1 = <specific definition of poor>

### 2. <Dimension Name>
...

(repeat for all dimensions)

## Output Format

Respond with ONLY a JSON object, no other text:

` ` `json
{
  "<dimension_snake_case>": { "score": <1-5>, "reasoning": "<one sentence>" },
  ...
  "total": <sum of all scores>,
  "max_possible": <N × 5>,
  "suggestions": ["<improvement 1>", "<improvement 2>"]
}
` ` `
```

### Rules for generating dimensions

- **Aim for 5–7 dimensions.** Fewer than 4 makes scoring too coarse; more than 8 adds noise.
- **Every dimension must be specific to what this command does.** Do not use generic dimensions like "overall quality".
- **Always include these universal dimensions** (adapted to the command's context):
  - **Structure / Format Compliance** — does the output match the expected format?
  - **Content Accuracy** — is the content faithful to inputs, with no hallucination?
  - **Conciseness** — is it appropriately tight, without filler?
- **Add command-specific dimensions** based on what the skill uniquely does. Examples:
  - `/commit` → "Conventional Format", "Scope Accuracy", "Body Detail"
  - `/story` → "Gherkin Syntax", "Acceptance Criteria Coverage", "Testability"
  - `/audit` → "Swagger Coverage", "Milestone Granularity", "Done-When Specificity"
- **The 1/3/5 anchors must be concrete and distinguishable.** A scorer should be able to read them and know exactly what score to give.
- **Dimension names in the JSON output must be snake_case versions of the heading names.**

---

## Step 4 — Generate fixtures

For each command, create `evals/fixtures/<command>/` with realistic sample input files.

1. **Read the skill file** to determine what files/inputs the command expects.
2. **Create sample files** that are:
   - Realistic — representative of actual project content, not trivial "hello world" examples.
   - Complex enough to exercise edge cases (e.g. multiple milestones, mixed requirement types).
   - Self-contained — no references to external files that won't exist during eval.
3. **Size guideline** — each fixture file should be 30–80 lines. Enough to be meaningful, not so large that it burns tokens.

If the command expects inputs that are hard to simulate as files (e.g. `git diff` output, API responses), create a text file containing a realistic sample and note in a `README.md` inside the fixtures directory how it should be used.

---

## Step 5 — Show results

After generating everything, show a summary per command:

```
✓ commit
  Created: evals/criteria/commit.md (6 dimensions, max score 30)
  Created: evals/fixtures/commit/sample-diff.txt
  Ready for: /evolve commit

✓ story
  Created: evals/criteria/story.md (5 dimensions, max score 25)
  Created: evals/fixtures/story/spec.md
  Ready for: /evolve story
```

---

## Step 6 — Offer next steps

Ask the user:
- **Review and edit the criteria?** (open the files for manual tweaking)
- **Run `/evolve` on these commands now?**
- **Done for now?**
