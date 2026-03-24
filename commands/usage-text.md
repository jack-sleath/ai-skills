Check the current Claude usage/quota and next reset time by scraping the Claude settings page and interpreting the result.

Arguments (optional): $ARGUMENTS

Interpret any arguments as flags to pass through to the Python script (e.g. `--profile-dir "Profile 1"`, `--headless`).

---

## Step 1 — Check prerequisites

Verify that `selenium` is installed:

```bash
python3 -c "import selenium" 2>/dev/null
```

If it fails, tell the user to install it: `pip install selenium` — and that they need chromedriver on their PATH.

---

## Step 2 — Fetch the page

Run the script to get the rendered page content:

```bash
python3 tools/read_usage.py --html $ARGUMENTS
```

The script opens Chrome with the user's existing profile (so they're already logged in), navigates to `https://claude.ai/settings/usage`, waits for it to render, and returns JSON with:
- `page_text` — the visible text content of the page
- `page_html` — the rendered HTML of the `<main>` element (when `--html` is passed)
- `status` — `ok`, `empty`, or `error`

If the script fails, show the error and suggest:
- Chrome might be open already — Selenium can't attach to a running Chrome with the same profile. Ask the user to close Chrome first, or use a different `--profile-dir`.
- chromedriver version might not match their Chrome version.

---

## Step 3 — Interpret the content

Read the `page_text` (and `page_html` if available) from the JSON output. You are looking for two things:

1. **Current usage** — a percentage, progress bar, or fraction showing how much of the user's quota has been used (e.g. "42% used", "58% remaining", a progress bar at some level).
2. **Next reset time** — when the usage limit resets (e.g. "Resets in 3h 42m", "Next reset: 2:00 PM", a countdown, a date/time).

Use your judgement to find these values — the page layout may change over time. Look at the full text and HTML structure rather than relying on exact strings.

---

## Step 4 — Present the results

Display a summary box. Adapt the content based on what you found:

```
┌─ Claude Usage ─────────────────────────────┐
│ Used:       42%                              │
│ Remaining:  58%                              │
│                                              │
│ ██████████████░░░░░░░░░░░░░░  42%           │
│                                              │
│ Next reset: in 3h 42m                        │
└──────────────────────────────────────────────┘
```

- The progress bar should be 28 characters wide. Fill `█` for the used portion and `░` for remaining.
- If you found a reset time, show the "Next reset" line. Convert ISO datetimes to a human-friendly relative format.
- If you could only find one of the two values, show what you have and note the other wasn't found.
- If neither was found, show the raw page text (truncated) so the user can debug.
