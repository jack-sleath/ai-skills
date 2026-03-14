#!/usr/bin/env bash
# Install AI Skills for Claude Code
# Creates symlinks from ~/.claude/commands/ to this repo's commands/

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMMANDS_SOURCE="$REPO_ROOT/commands"
COMMANDS_DEST="$HOME/.claude/commands"

# Create destination if it doesn't exist
mkdir -p "$COMMANDS_DEST"

# Symlink each .md file
count=0
for skill in "$COMMANDS_SOURCE"/*.md; do
    [ -f "$skill" ] || continue
    name="$(basename "$skill")"
    ln -sf "$skill" "$COMMANDS_DEST/$name"
    echo "Linked: $name"
    ((count++))
done

if [ "$count" -eq 0 ]; then
    echo "No skills found in $COMMANDS_SOURCE"
else
    echo -e "\nDone. $count skill(s) installed."
fi
