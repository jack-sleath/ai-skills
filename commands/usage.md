Check the current Claude usage/quota by running the `read_usage.py` tool and presenting the results.

Arguments (optional): $ARGUMENTS

Interpret any arguments as flags to pass through (e.g. `--profile-dir "Profile 1"`, `--headless`).

---

## Step 1 — Check prerequisites

Verify that `selenium` is installed:

```bash
python3 -c "import selenium" 2>/dev/null
```

If it fails, tell the user to install it: `pip install selenium` — and that they need chromedriver on their PATH.

---

## Step 2 — Run the script

Run the usage reader in JSON mode so you can parse the output:

```bash
python3 tools/read_usage.py --json $ARGUMENTS
```

If the script exits with a non-zero code, show the error and suggest:
- Chrome might be open already — Selenium can't attach to a running Chrome with the same profile. Ask the user to close Chrome first, or use a different `--profile-dir`.
- chromedriver version might not match their Chrome version.

---

## Step 3 — Present the results

Parse the JSON output. Display a summary like this:

```
┌─ Claude Usage ─────────────────────┐
│ Used:       42%                     │
│ Remaining:  58%                     │
│                                     │
│ ██████████████░░░░░░░░░░░░░░  42%  │
│                                     │
│ Status: OK                          │
└─────────────────────────────────────┘
```

The progress bar should be 28 characters wide. Fill `█` for the used portion and `░` for remaining.

If the status is `not_found`, tell the user the script couldn't locate a percentage on the page — the Claude UI may have changed. Suggest running with `--headless` disabled and checking the page manually.
