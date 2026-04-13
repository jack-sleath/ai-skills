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
| Commit | `/commit` | Reviews current changes and creates a well-crafted local git commit |
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
| Browser Task | `/browser-task` | Generates a prompt for the Claude web extension to perform a browser-based task, with output as a downloadable `.md` file you can feed back into the terminal |
| To Browser | `/to-browser` | Extracts instructions from the current conversation and packages them as a `/browser-task` prompt for the Claude web extension |
| As A | `/as-a <role> [task]` | Adopts a professional role (e.g. qa, reviewer, tech-lead) from `roles/` and approaches the task through that lens |
| Create Criteria | `/create-criteria [command(s)]` | *(repo-local)* Scaffolds eval criteria and test fixtures for one or more commands so they can be used with `/evolve` |
| Evolve | `/evolve [command(s)] [--runs N] [--score N] [--model M] [--optimize O]` | *(repo-local)* Runs the self-evolution eval loop for one or more commands — executes against test fixtures, scores output, and iteratively improves prompts. Batch mode accepts a comma/space-separated list of commands |

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

## Self-Evolving Skills

The `/evolve` command runs an automated eval loop that scores a skill's output against a rubric and iteratively rewrites the skill prompt to improve it. Think of it as automated prompt engineering.

### Quick Start

1. **Install the Python dependency:**
   ```bash
   pip install anthropic
   ```

2. **Set your API key:**
   ```bash
   export ANTHROPIC_API_KEY=sk-ant-...
   ```

3. **Run the evolve skill** (the `/feature` command has eval support out of the box):
   ```
   /evolve feature
   ```
   Claude will ask you for iteration count, model, and optimisation target, then run the loop.

4. **Or run the eval script directly** (bypasses the interactive skill):
   ```bash
   python3 evals/run.py feature --evolve --runs 3
   ```

### Adding Eval Support to Another Command

To make any other skill self-evolvable, create two things:

1. **A criteria file** — `evals/criteria/<command>.md`
   - Defines scoring dimensions (each scored 1–5) that describe what good output looks like.
   - Must end with an output format section specifying a JSON schema for scores.
   - See `evals/criteria/feature.md` for a working example.

2. **A fixtures directory** — `evals/fixtures/<command>/`
   - Contains sample project files that simulate realistic input the command would normally see.
   - These are fed to the API in place of a real project, so they should be representative.
   - See `evals/fixtures/feature/` for a working example (contains `ACCEPTANCE_CRITERIA.md` and `MILESTONES.md`).

Once both exist, `/evolve <command>` will pick them up automatically.

### How It Works

Each iteration runs a three-stage pipeline:

```
1. EXECUTE — Feed the skill prompt + fixtures to the API → get output
2. SCORE   — Feed the output + criteria to the API → get scores (JSON)
3. EVOLVE  — Feed the skill + scores + output to the API → get improved skill prompt
```

The evolved prompt is written back to `commands/<command>.md`. The original can always be restored with `git checkout commands/<command>.md`.

### Optimisation Modes

| Mode | What it does |
|---|---|
| `score` (default) | Maximise eval score — fix the lowest-scoring dimensions |
| `tokens` | Reduce token usage while keeping score above a floor |
| `both` | Improve score AND reduce tokens in one pass |

**Recommended workflow:** Run `score` first until the score plateaus, then switch to `tokens` to make the prompt leaner without losing quality.

### Commands Currently Supporting Eval

| Command | Criteria | Fixtures |
|---|---|---|
| `/feature` | `evals/criteria/feature.md` | `evals/fixtures/feature/` |

For full details on the eval framework, see [`evals/README.md`](evals/README.md).

## Structure

```
ai-skills/
  commands/       # Claude Code skill .md files
  roles/          # Professional role definitions for /as-a
  evals/          # Self-evolution eval framework
    criteria/     # Per-command scoring rubrics (.md)
    fixtures/     # Test inputs per command (subdirectory each)
    results/      # Run logs with scores and token usage (.json)
    run.py        # API-based eval runner with token tracking
  ps-commands/    # PowerShell / shell function .ps1 / .sh files
  install.ps1     # Windows installer
  install.sh      # Linux/macOS installer
```
