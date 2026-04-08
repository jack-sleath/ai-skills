Analyse this project's git history to estimate how much time has been spent on it.

Arguments (optional): $ARGUMENTS

Run the Python script to generate the estimate:

```
python ~/.claude/scripts/estimate_time.py $ARGUMENTS
```

The script handles argument parsing (no args, relative periods like `3 months`, single date, or date range), git log retrieval, session grouping, and duration calculation.

Present the script's Markdown output directly to the user. Only add commentary if:
- Two contributor names look like the same person (different git configs) — mention this
- The date range seems surprising given the arguments
- The user asks follow-up questions
