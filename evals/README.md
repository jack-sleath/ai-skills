# Self-Evolution Eval Framework

This document explains how the eval runner works so that an LLM (you) can understand and operate it.

## What This Does

The eval framework tests a Claude Code skill command against fixture files, scores the output against a rubric, and optionally loops to improve the command prompt automatically. Think of it as automated prompt engineering — run, score, rewrite, repeat.

## Directory Layout

```
evals/
  run.py              # The eval runner script (Python, calls Anthropic API)
  criteria/<cmd>.md   # Scoring rubric for each command (dimensions, 1-5 scale)
  fixtures/<cmd>/     # Test input files that simulate a real project
  results/            # JSON output from each iteration (auto-generated)
```

## Prerequisites

Before running, three things must exist for the target command:

1. **Command file** — `commands/<command>.md` (the skill to evaluate/evolve)
2. **Criteria file** — `evals/criteria/<command>.md` (defines what "good output" looks like, with scoring dimensions)
3. **Fixtures directory** — `evals/fixtures/<command>/` (contains the project files the command will be run against)

The `claude` CLI must be installed and available on the PATH (no API key needed).

## How a Single Eval Works

Each iteration runs a three-stage pipeline:

```
1. EXECUTE — Feed the command + fixtures to the API, get output
2. SCORE   — Feed the output + criteria to the API, get scores (JSON)
3. EVOLVE  — Feed the command + scores + output to the API, get improved command
```

Stage 3 only runs if `--evolve` is passed. Without it, you just get a score.

## Running the Script

```bash
# Single eval (no evolution) — just score the current command
python3 evals/run.py feature

# Evolve for score (default) — 3 iterations improving quality
python3 evals/run.py feature --evolve --runs 3

# Evolve for token efficiency — reduce tokens while maintaining score
python3 evals/run.py feature --evolve --optimize tokens

# Evolve for both — improve score AND reduce tokens
python3 evals/run.py feature --evolve --optimize both

# Set an explicit score floor for token optimisation
python3 evals/run.py feature --evolve --optimize tokens --min-score 20

# Use a different model
python3 evals/run.py feature --evolve --model claude-opus-4-6

# Dry run — print prompt length without calling the API
python3 evals/run.py feature --dry-run
```

## The `--optimize` Flag

This controls what the evolution prompt tells the API to focus on:

| Mode | Behaviour |
|---|---|
| `score` (default) | Improve the lowest-scoring dimensions. Ignore token count. |
| `tokens` | Reduce token usage (concise phrasing, remove redundancy) while keeping total score at or above a threshold. |
| `both` | Fix lowest-scoring dimensions first, but also tighten the prompt wherever possible. |

When optimising for `tokens` or `both`, a minimum score floor is enforced. If `--min-score` is not provided, the framework uses the iteration-1 score as the floor automatically.

## Recommended Workflow

The intended workflow is two phases:

1. **Phase 1 — Optimise for score.** Run `--optimize score` (or just `--evolve`) until the score plateaus or hits the maximum. This gets the command producing high-quality output.

2. **Phase 2 — Optimise for tokens.** Switch to `--optimize tokens`. The iteration-1 score becomes the floor. The evolution prompt now focuses on making the command leaner — removing redundant instructions, combining steps, cutting verbose phrasing — without dropping below the quality baseline.

You can also run `--optimize both` if you want to do both in a single pass, though the two-phase approach gives more control.

## What the Output Looks Like

Each iteration prints:

```
============================================================
  Iteration 1 of 3
============================================================
  Running command...
  Scoring output...

  Scores:
    Structure Compliance: 4/5 — follows template correctly
    Content Accuracy: 3/5 — minor hallucination in KPIs
    TOTAL: 22/30
    Suggestions:
      - Ground KPIs in source material

  Token Usage:
    Tokens — in: 3,200  out: 1,800  total: 5,000

  Result saved to feature_iter1_20260323T120000Z.json
  Evolving command...
  Command updated (2,100 tokens)
```

After all iterations, a summary shows the trend:

```
============================================================
  Evolution Summary
============================================================
    Iteration 1: 22/30 (5,000 tokens)
    Iteration 2: 26/30 (4,800 tokens)
    Iteration 3: 28/30 (4,200 tokens)

    Score change: +6 (22 → 28)
    Exec tokens change: -800 (5,000 → 4,200)
    Total tokens used: 18,300
```

## Result Files

Each iteration saves a JSON file to `evals/results/` with this structure:

```json
{
  "command": "feature",
  "model": "claude-sonnet-4-6",
  "iteration": 1,
  "command_content": "<the skill .md content used>",
  "command_output": "<what the API produced>",
  "scores": {
    "Structure Compliance": { "score": 4, "reasoning": "..." },
    "total": 22,
    "max_possible": 30,
    "suggestions": ["..."]
  },
  "token_usage": {
    "execution": { "input_tokens": 2000, "output_tokens": 1200, "total_tokens": 3200 },
    "scoring": { "input_tokens": 1000, "output_tokens": 800, "total_tokens": 1800 },
    "combined": { "input_tokens": 3000, "output_tokens": 2000, "total_tokens": 5000 },
    "evolution": { "input_tokens": 1500, "output_tokens": 600, "total_tokens": 2100 }
  }
}
```

## Important Notes

- The script **overwrites** `commands/<command>.md` after each evolution step. The original can be restored with `git checkout commands/<command>.md`.
- Evolution modifies the prompt instructions, not the criteria or fixtures.
- Token usage in "execution" reflects what the command itself costs to run — this is what `--optimize tokens` tries to reduce.
- The "scoring" and "evolution" token costs are overhead of the eval process itself, not the command's runtime cost.
