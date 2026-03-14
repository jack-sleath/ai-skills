# Install AI Skills for Claude Code
# Creates symlinks from ~/.claude/commands/ to this repo's commands/
# Requires: Developer Mode enabled, or run as Administrator

$repoRoot = $PSScriptRoot
$commandsSource = Join-Path $repoRoot "commands"
$commandsDest = Join-Path $HOME ".claude\commands"

# Create destination if it doesn't exist
if (-not (Test-Path $commandsDest)) {
    New-Item -ItemType Directory -Path $commandsDest -Force | Out-Null
    Write-Host "Created $commandsDest"
}

# Symlink each .md file
$skills = Get-ChildItem -Path $commandsSource -Filter "*.md"

if ($skills.Count -eq 0) {
    Write-Host "No skills found in $commandsSource"
    exit 0
}

foreach ($skill in $skills) {
    $linkPath = Join-Path $commandsDest $skill.Name
    $targetPath = $skill.FullName

    if (Test-Path $linkPath) {
        Remove-Item $linkPath -Force
    }

    New-Item -ItemType SymbolicLink -Path $linkPath -Target $targetPath | Out-Null
    Write-Host "Linked: $($skill.Name)"
}

Write-Host "`nDone. $($skills.Count) skill(s) installed."
