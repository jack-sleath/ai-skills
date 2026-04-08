Check the current Claude usage/quota and next reset time by fetching the Claude settings page and interpreting the result.

Arguments (optional): $ARGUMENTS

---

## Step 1 — Fetch the page

Use the WebFetch tool to retrieve the Claude usage page:

```
URL: https://claude.ai/settings/usage
```

Save the fetched content to a temporary file, then run the parser:

```
python ~/.claude/scripts/usage_check.py <temp_file>
```

## Step 2 — Present the results

Display the script's output directly — it produces a formatted summary box with usage percentage, progress bar, and reset time.

If the WebFetch fails or returns an empty/login page, tell the user that the page could not be accessed and they may need to check their usage manually at https://claude.ai/settings/usage.
