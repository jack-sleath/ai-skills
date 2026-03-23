You are running the self-evolution eval loop for a skill command.

---

## Step 1 — Pick the command

If the user provided a command name as an argument (e.g. `/evolve feature`), use that. Otherwise, list the available commands in `commands/` (excluding this file) and ask the user to pick one.

---

## Step 2 — Check prerequisites

Verify that the following exist:
- `evals/criteria/<command>.md` — the scoring rubric for the chosen command
- `evals/fixtures/<command>/` — a directory with at least one fixture file

If either is missing, tell the user and stop. Explain that they need to create a criteria file and fixtures before evolving a command.

Also verify that the `ANTHROPIC_API_KEY` environment variable is set. If not, tell the user to set it.

---

## Step 3 — Ask for parameters

Ask the user:
1. **How many iterations?** (default: 3)
2. **Which model?** (default: `claude-sonnet-4-6` — cheaper for iteration; suggest `claude-opus-4-6` for final quality runs)

---

## Step 4 — Run the eval loop

Run the eval script:

```bash
python3 evals/run.py <command> --evolve --runs <N> --model <model>
```

Stream the output to the user so they can watch progress.

---

## Step 5 — Review results

After the loop completes:

1. Read the latest result files from `evals/results/`.
2. Show the user a summary table:
   - Iteration number
   - Score per dimension
   - Total score
   - Token usage (input / output / total)
   - Score delta from previous iteration
3. If the score improved, show the diff of changes made to the command file.
4. If the score decreased on any iteration, flag it — the user may want to revert.

---

## Step 6 — Confirm or revert

Ask the user:
- **Keep the evolved command?** (the file has already been updated)
- **Revert to the original?** (restore from git: `git checkout commands/<command>.md`)
- **Try more iterations?**

If the user wants to revert, run `git checkout commands/<command>.md` to restore the original.
