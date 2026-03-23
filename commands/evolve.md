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
3. **Optimisation target?**
   - `score` (default) — maximise eval score, ignore token count
   - `tokens` — reduce token usage while keeping score above a threshold
   - `both` — improve score AND reduce tokens simultaneously
4. **Minimum score threshold?** (only when optimising for `tokens` or `both`; defaults to the iteration-1 score as a floor)

---

## Step 4 — Run the eval loop

Run the eval script:

```bash
python3 evals/run.py <command> --evolve --runs <N> --model <model> --optimize <target>
```

If the user chose `tokens` or `both`, also pass `--optimize tokens` (or `--optimize both`). If a minimum score threshold was specified, pass `--min-score <value>`.

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

## Step 5b — Cost estimate

After showing the results table, display a **Cost Estimate** box summarising the total resource usage:

1. **API tokens** — sum the `total_tokens` from every iteration's result JSON (the `combined` and `evolution` usage fields). This is exact.
2. **Estimated session tokens** — estimate the Claude Code session overhead (this skill's own orchestration) at roughly **2,000 tokens per iteration** (reading files, asking questions, displaying output). This is approximate.
3. **Grand total** — API tokens + estimated session tokens.
4. **Approximate cost** — calculate using these per-token rates (input ≈ $3/M tokens, output ≈ $15/M tokens for Sonnet; input ≈ $15/M, output ≈ $75/M for Opus). If the exact split is unknown, use the blended rate of $8/M tokens for Sonnet or $40/M tokens for Opus.

Display it like this:

```
┌─ Cost Estimate ──────────────────────────────┐
│ API tokens (exact):       45,230             │
│ Session overhead (est.):  ~6,000             │
│ Grand total:              ~51,230 tokens     │
│ Estimated API cost:       ~$0.36 (sonnet)    │
│ Note: Session overhead is a rough estimate.  │
│ Use /cost for precise API-user billing.      │
└──────────────────────────────────────────────┘
```

This gives the user a ballpark sense of what each evolve run costs in tokens and dollars.

---

## Step 6 — Confirm or revert

Ask the user:
- **Keep the evolved command?** (the file has already been updated)
- **Revert to the original?** (restore from git: `git checkout commands/<command>.md`)
- **Try more iterations?**

If the user wants to revert, run `git checkout commands/<command>.md` to restore the original.
