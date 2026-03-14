#!/usr/bin/env bash
# Install AI Skills
# 1. Creates symlinks from ~/.claude/commands/ to this repo's commands/
# 2. Adds a shell loader for ps-commands/ to ~/.bashrc and/or ~/.zshrc

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── Claude Code skills ──────────────────────────────────────────────────────
COMMANDS_SOURCE="$REPO_ROOT/commands"
COMMANDS_DEST="$HOME/.claude/commands"

mkdir -p "$COMMANDS_DEST"

count=0
for skill in "$COMMANDS_SOURCE"/*.md; do
    [ -f "$skill" ] || continue
    name="$(basename "$skill")"
    ln -sf "$skill" "$COMMANDS_DEST/$name"
    echo "Linked (Claude): $name"
    ((count++))
done

if [ "$count" -eq 0 ]; then
    echo "No Claude skills found in $COMMANDS_SOURCE"
else
    echo "Done. $count Claude skill(s) installed."
fi

# ── Shell commands ──────────────────────────────────────────────────────────
PS_COMMANDS_SOURCE="$REPO_ROOT/ps-commands"
MARKER="AI Skills - shell commands loader"

LOADER_BLOCK="
# $MARKER
# Source: $PS_COMMANDS_SOURCE
for f in \"$PS_COMMANDS_SOURCE\"/*.sh; do
    [ -f \"\$f\" ] && . \"\$f\"
done"

add_loader_to() {
    local rc_file="$1"
    if [ -f "$rc_file" ] && grep -q "$MARKER" "$rc_file" 2>/dev/null; then
        echo "Shell loader already present in $rc_file"
    else
        printf '%s\n' "$LOADER_BLOCK" >> "$rc_file"
        echo "Added shell loader to $rc_file"
    fi
}

[ -f "$HOME/.bashrc" ] && add_loader_to "$HOME/.bashrc"
[ -f "$HOME/.zshrc" ]  && add_loader_to "$HOME/.zshrc"

echo -e "\nAll done. Restart your shell (or run 'source ~/.bashrc') to load ps-commands."
