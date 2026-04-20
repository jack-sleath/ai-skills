List all open pull requests across the current org/user (not just this repo) that were not created by you, from the last 3 weeks, ordered oldest first, with line change stats.

Run the Python script to generate the list:

```
python ~/.claude/scripts/open_prs.py
```

The script handles GitHub user detection, org detection from the current repo, PR search, filtering, date sorting, and diff line counting.

Present the script's Markdown output directly to the user. Only add commentary if:
- The user asks follow-up questions
- The script errors out — explain what went wrong
