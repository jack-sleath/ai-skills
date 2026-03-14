# AI Skills

A portable collection of custom Claude Code skills, installable across multiple machines via symlinks.

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

## Structure

```
ai-skills/
  commands/       # skill .md files
  install.ps1     # Windows installer
  install.sh      # Linux/macOS installer
```
