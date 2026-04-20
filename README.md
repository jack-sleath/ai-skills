# AI Skills

A portable collection of custom Claude Code skills, installable across multiple machines via symlinks.

## Skills

| Skill | Command | Description |
|---|---|---|
| Invest Idea | `/invest-idea` | Fleshes out a software idea into a plan via guided Q&A, generating `ACCEPTANCE_CRITERIA.md` and `MILESTONES.md` |
| Feature | `/feature` | Generates a `FEATURE.md` document from `MILESTONES.md` and `ACCEPTANCE_CRITERIA.md`, filling in what it can and asking for the rest |
| Milestone | `/milestone` | Implements the next incomplete milestone from `MILESTONES.md`, creates a git branch, commits, and pushes |
| Stories | `/stories` | Generates a Gherkin story card for every milestone in `MILESTONES.md` and writes them to `stories/milestone-N.md` |
| Story | `/story` | Generates a single Gherkin story card (title, technical notes, acceptance criteria) from a given specification |
| Commit | `/commit` | Reviews current changes, groups related files into logical batches, and creates one commit per batch |
| Branch For | `/branch-for <base-branch>` | Creates a dated staging branch off a target base, merges the current feature branch in, and opens a PR |
| Select Branch | `/select-branch [prompt]` | Interactively picks a remote branch using fzf (or a numbered list fallback) and returns the selection |
| Branch UAT | `/branch-uat` | Shortcut for `/branch-for UAT/main` — creates a `UAT/XXXXX-YYYY-MM-DD` branch and PR |
| Branch Develop | `/branch-develop` | Shortcut for `/branch-for develop` — creates a `develop-XXXXX-YYYY-MM-DD` branch and PR |
| Estimate Time | `/estimate-time [period]` | Analyses git history to estimate time spent. Accepts a date range, single date, or relative period (e.g. `3 months`, `30 days`) |
| Ship | `/ship` | Implements all incomplete milestones in sequence — after each one, raises a PR to main and immediately starts the next |
| Feedback | `/feedback` | Translates feedback or a change request into a plan — appends to `ACCEPTANCE_CRITERIA.md` and `MILESTONES.md`, and creates a `<CHANGE-TITLE>_FEATURE.md` |
| Merge From | `/merge-from <branch>` | Fetches a branch from origin and merges it into the current active branch |
| Tidy Branches | `/tidy-branches` | Switches to main/master, fetches latest, and deletes all local branches that have been pushed to the remote |
| Audit | `/audit` | Reverse-engineers `ACCEPTANCE_CRITERIA.md` and `MILESTONES.md` (Milestone 0) from an existing project's Swagger definitions, unit tests, and optional Gherkin — one set of files per VS project if a solution is present |
| Browser Task | `/browser-task` | Generates a prompt for the Claude web extension to perform a browser-based task (auto-copied to clipboard), with output as a downloadable `.md` file you can feed back into the terminal |
| To Browser | `/to-browser` | Extracts instructions from the current conversation, confirms them, then delegates to `/browser-task` to generate and clipboard-copy the prompt — no re-asking |
| As A | `/as-a <role> [task]` | Adopts a professional role (e.g. qa, reviewer, tech-lead) from `roles/` and approaches the task through that lens |
| Branch Drift | `/branch-drift` | Checks all repos in the current org for branches that have drifted ahead of their downstream (e.g. main ahead of develop) |
| Open PRs | `/open-prs` | Lists open PRs by others across the current org/user from the last 3 weeks — oldest first, with line change stats and links |
| Review PR | `/review-pr` | Picks a PR from the `/open-prs` list, reviews it in the terminal, and optionally posts the review as a PR comment |
| Review PRs | `/review-prs` | Reviews all open PRs in the current repo with fresh eyes, reports issues grouped by severity, and offers to fix them |
| Cook Story | `/cook-story <notion-link> <iteration>` | Fetches a Notion spec, generates a Gherkin story card, and creates a Shortcut story in the given iteration |
| Who Is In Charge | `/who-is-in-charge` | Picks a random handle (emoji + name) from `~/.claude/who-is-in-charge.json` and auto-copies a `/rename` line to your clipboard so you can paste it straight into the prompt — swaps the handle on repeat runs rather than stacking |

## Setup

### Windows

```powershell
git clone <repo-url>
cd ai-skills
.\install.ps1
```

### Linux / macOS

```bash
git clone <repo-url>
cd ai-skills
chmod +x install.sh
./install.sh
```

## Updating

Run the installer again after pulling, or just double-click `install-admin.bat` which does both:

```bash
git pull
```

## Adding a Claude skill

Create a `.md` file in `commands/`. See the [Claude Code docs](https://docs.anthropic.com/en/docs/claude-code/slash-commands) for the skill format, then re-run the install script to link it.

Remember to update the **Skills** table in this README with the new skill's command and description.

## Adding a PowerShell command

Create a `.ps1` file in `ps-commands/`. Each file should define one function with the same name as the file (e.g. `ps-commands/greet.ps1` defines `function greet { ... }`).

The install script adds a profile loader that auto-sources all `.ps1` files in `ps-commands/` on shell start — so after a `git pull` your new commands are available immediately without reinstalling.

On Linux/macOS, add `.sh` files to `ps-commands/` instead — they are sourced the same way via `~/.bashrc` / `~/.zshrc`.

## Structure

```
ai-skills/
  commands/       # Claude Code skill .md files
  roles/          # Professional role definitions for /as-a
  data/           # Seed JSON files copied to ~/.claude/ on install (merged by `name` key for array-of-object JSON — user edits and locally-added entries preserved; new seed entries appended)
  evals/          # Self-evolution eval framework
    criteria/     # Per-command scoring rubrics (.md)
    fixtures/     # Test inputs per command (subdirectory each)
    results/      # Run logs with scores and token usage (.json)
    run.py        # API-based eval runner with token tracking
  ps-commands/    # PowerShell / shell function .ps1 / .sh files
  scripts/        # Python helper scripts copied to ~/.claude/scripts/ on install
  install.ps1     # Windows installer
  install.sh      # Linux/macOS installer
```
