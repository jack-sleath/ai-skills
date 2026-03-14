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
| Branch UAT | `/branch-uat` | Shortcut for `/branch-for UAT/main` — creates a `UAT/XXXXX-YYYY-MM-DD` branch and PR |
| Branch Develop | `/branch-develop` | Shortcut for `/branch-for develop` — creates a `develop-XXXXX-YYYY-MM-DD` branch and PR |
| Estimate Time | `/estimate-time [period]` | Analyses git history to estimate time spent. Accepts a date range, single date, or relative period (e.g. `3 months`, `30 days`) |

## Setup

### Windows
> Requires Developer Mode enabled (Settings → System → For developers) or run as Administrator.

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

Pull the latest changes — symlinks mean no reinstall needed:

```bash
git pull
```

## Adding a skill

Create a `.md` file in `commands/`. See the [Claude Code docs](https://docs.anthropic.com/en/docs/claude-code/slash-commands) for the skill format, then re-run the install script to link it.

Remember to update the **Skills** table in this README with the new skill's command and description.

## Structure

```
ai-skills/
  commands/       # skill .md files
  install.ps1     # Windows installer
  install.sh      # Linux/macOS installer
```
