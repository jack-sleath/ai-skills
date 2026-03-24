You are running the self-evolution eval loop for one or more skill commands.

---

## Step 0 — Detect mode

Check the arguments the user passed:

- **Single command** — e.g. `/evolve feature` → single mode (Steps 1–6 as before)
- **Multiple commands** — e.g. `/evolve feature,commit,story --runs 5` or `/evolve feature commit story --score 4.0` → batch mode (go to Step B1)
- **No arguments** — ask the user to pick a command, then single mode

### Argument parsing

| Flag | Meaning | Default |
|---|---|---|
| `--runs N` | Max iterations per command | 3 |
| `--score N%` | Stop early when score ≥ N% (e.g. `--score 85%`) | _(no limit — run all iterations)_ |
| `--model M` | Model to use | `claude-sonnet-4-6` |
| `--optimize O` | `score`, `tokens`, or `both` | `score` |

Commands can be separated by commas or spaces. The flags apply to every command in the batch.

---

## Step 1 — Pick the command (single mode)

If the user provided a single command name as an argument (e.g. `/evolve feature`), use that. Otherwise, list the available commands in `commands/` (excluding this file) and ask the user to pick one.

---

## Step 2 — Check prerequisites

Verify that the following exist for the target command (or every command in batch mode):
- `evals/criteria/<command>.md` — the scoring rubric for the chosen command
- `evals/fixtures/<command>/` — a directory with at least one fixture file

If either is missing, tell the user and stop (single mode) or skip that command with a warning (batch mode).

Also verify that the `claude` CLI is available on the PATH. If not, tell the user to install Claude Code.

---

## Step 3 — Ask for parameters (single mode only)

In single mode, ask the user if they didn't already pass flags:
1. **How many iterations?** (default: 3)
2. **Which model?** (default: `claude-sonnet-4-6` — cheaper for iteration; suggest `claude-opus-4-6` for final quality runs)
3. **Optimisation target?**
   - `score` (default) — maximise eval score, ignore token count
   - `tokens` — reduce token usage while keeping score above a threshold
   - `both` — two-phase: first maximise score (up to 100%, or `--score` target if given), then use remaining runs to minimise token usage
4. **Minimum score threshold?** (only when optimising for `tokens`; defaults to the iteration-1 score as a floor)

In batch mode, all parameters come from the flags — do not ask interactively.

---

## Step 4 — Run the eval loop

Run the eval script:

```bash
python3 evals/run.py <command> --evolve --runs <N> --model <model> --optimize <target>
```

If the user chose `tokens`, also pass `--optimize tokens`. If a minimum score threshold was specified, pass `--min-score <value>`.

**Early stop on `--score`:** After each iteration, read the result JSON to get `total` and `max_possible`. Calculate the percentage: `(total / max_possible) × 100`. If it meets or exceeds the `--score` threshold, stop iterating for this command and move on. This means `--score 85%` works consistently regardless of whether a command has 5, 6, or 7 dimensions.

**Two-phase loop for `--optimize both`:**
- **Phase 1 — Score:** Run iterations passing `--optimize score`. Stop phase 1 when the score reaches 100%, or when the `--score` target is met if one was given, or when runs are exhausted.
- **Phase 2 — Tokens:** If runs remain after phase 1, switch to passing `--optimize tokens` (with `--min-score` set to the score achieved at the end of phase 1 as the floor). Stop phase 2 early if the token reduction from the previous best is less than 5% (negligible — within natural run-to-run variance), or when runs are exhausted.
- Show a phase header in the streamed output so the user can see when the switch happens.

**Best-version tracking:** After each iteration, compare the score (or token count in phase 2) to the current best. If the new iteration is worse, revert the command file to the best version before the next iteration so evolution always builds on the best result so far, not a regression. Keep track of which iteration produced the best result.

Stream the output to the user so they can watch progress.

---

## Step 5 — Review results

After the loop completes:

1. Read the latest result files from `evals/results/`.
2. Show the user a summary table:
   - Iteration number
   - Score per dimension
   - Total score (raw and percentage, e.g. `26/30 — 87%`)
   - Token usage (input / output / total)
   - Score delta from previous iteration
3. Ensure the command file is set to the best-scoring version (it should already be, due to best-version tracking in Step 4, but verify).
4. Show the diff of changes between the original and the best version.
5. If the best version came from an earlier iteration (i.e. later runs regressed), note which iteration it was.

---

## Step 5b — Usage check

After showing the results table, check how much of the user's Claude quota was consumed by running `/usage-text`. This delegates to `tools/read_usage.py` which loads the Claude usage page via Selenium and returns the rendered page content.

Run the script directly (no need to invoke the full `/usage-text` skill):

```bash
python3 tools/read_usage.py --html
```

Parse the JSON output. Read `page_text` (and `page_html` if needed) to find the **current usage percentage**. Ignore reset time for now.

Then display a box combining the API token totals from the eval results with the live quota reading:

```
┌─ Usage Summary ──────────────────────────────┐
│ API tokens this run:  45,230                  │
│                                               │
│ Account quota:                                │
│ ██████████████░░░░░░░░░░░░░░  42% used       │
│                                               │
└───────────────────────────────────────────────┘
```

- **API tokens this run** — sum the `total_tokens` from every iteration's result JSON (the `combined` and `evolution` usage fields).
- **Account quota** — the usage percentage read from the page. Progress bar should be 28 characters wide (`█` for used, `░` for remaining).

If the script fails (e.g. Chrome is open, Selenium not installed), show the API token total and note that the live usage check was skipped, with a hint to try `/usage-text` manually.

---

## Step 6 — Confirm or revert

**Single mode:** Ask the user:
- **Keep the evolved command?** (the file has already been updated)
- **Revert to the original?** (restore from git: `git checkout commands/<command>.md`)
- **Try more iterations?**

If the user wants to revert, run `git checkout commands/<command>.md` to restore the original.

**Batch mode:** Skip this step — all changes are kept. The user can selectively revert after reviewing the batch summary.

---

## Batch mode steps

### Step B1 — Validate the batch

1. Parse the command list and flags from the arguments (see Step 0 for flag definitions).
2. Run Step 2 (prerequisite check) for every command in the list. Collect two lists: **ready** and **skipped**.
3. If any commands were skipped, show them with the reason (missing criteria, missing fixtures).
4. If no commands are ready, stop.
5. Show the batch plan and ask for confirmation:

```
Batch evolve plan:
  Commands:  feature, commit, story
  Runs:      5 per command (or until score ≥ 85%)
  Model:     claude-sonnet-4-6
  Optimize:  score

  Skipped:   audit (no criteria file)

Proceed? (y/n)
```

### Step B2 — Run the batch

For each ready command, in order:

1. Show a header: `── Evolving: <command> (N of M) ──`
2. Run Step 4 (eval loop) with the batch parameters.
   - If `--score` was given and a run meets the threshold, stop early for this command and note "passed" in the results.
3. Run Step 5 (review results) — show the per-command summary table.
4. Move to the next command.

Do **not** ask for confirmation between commands — just proceed.

### Step B3 — Batch summary

After all commands have been processed, show a single summary table:

```
┌─ Batch Results ──────────────────────────────────────────────────┐
│ Command     Iterations   Score         Status                    │
│ ─────────   ──────────   ───────────   ──────────────────────    │
│ feature     3 of 5       26/30 (87%)   ✓ passed (≥ 85%)         │
│ commit      5 of 5       24/30 (80%)   ✗ did not reach 85%      │
│ story       2 of 5       22/25 (88%)   ✓ passed (≥ 85%)         │
│                                                                  │
│ Total API tokens: 134,520                                        │
└──────────────────────────────────────────────────────────────────┘
```

- Scores are shown as `raw/max (percentage)` so differences in dimension count are visible.
- If `--score` was not given, the Status column shows just `done` for every command.
- Sum the API tokens across all commands.

### Step B4 — Batch usage check

Run the usage check from Step 5b once (not per command) to show the account quota after the full batch.

Then ask the user:
- **Keep all changes?**
- **Revert specific commands?** (list them — run `git checkout commands/<command>.md` for each)
- **Revert all?**
