Check the current Claude usage/quota and next reset time by fetching the Claude settings page and interpreting the result.

Arguments (optional): $ARGUMENTS

---

## Step 1 — Fetch the page

Use the WebFetch tool to retrieve the Claude usage page:

```
URL: https://claude.ai/settings/usage
```

Read the returned content to find usage information.

If the fetch fails or returns an empty/login page, tell the user that the page could not be accessed and they may need to check their usage manually at https://claude.ai/settings/usage.

---

## Step 2 — Interpret the content

You are looking for two things:

1. **Current usage** — a percentage, progress bar, or fraction showing how much of the user's quota has been used (e.g. "42% used", "58% remaining", a progress bar at some level).
2. **Next reset time** — when the usage limit resets (e.g. "Resets in 3h 42m", "Next reset: 2:00 PM", a countdown, a date/time).

Use your judgement to find these values — the page layout may change over time. Look at the full text and HTML structure rather than relying on exact strings.

---

## Step 3 — Present the results

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
