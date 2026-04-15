Check all repositories in the current org/user for branches that have drifted ahead of their expected downstream branch.

Run the Python script to generate the report:

```
python ~/.claude/scripts/branch_drift.py
```

The script handles org detection from the current repo, repo listing, branch comparison via the GitHub API, and Markdown output.

Present the script's Markdown output directly to the user. Only add commentary if:
- The user asks follow-up questions
- The script errors out — explain what went wrong
