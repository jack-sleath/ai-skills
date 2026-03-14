# Install AI Skills
# 1. Copies commands/ .md files to ~/.claude/commands/
# 2. Adds a PowerShell profile loader for ps-commands/
# No elevation required.

param(
    [switch]$ProfileOnly,
    [switch]$CommandsOnly
)

$repoRoot = $PSScriptRoot

# ── Claude Code skills ──────────────────────────────────────────────────────
if (-not $ProfileOnly) {
    $commandsSource = Join-Path $repoRoot "commands"
    $commandsDest = Join-Path $HOME ".claude\commands"

    if (-not (Test-Path $commandsDest)) {
        New-Item -ItemType Directory -Path $commandsDest -Force | Out-Null
        Write-Host "Created $commandsDest"
    }

    $skills = Get-ChildItem -Path $commandsSource -Filter "*.md"

    if ($skills.Count -eq 0) {
        Write-Host "No Claude skills found in $commandsSource"
    } else {
        foreach ($skill in $skills) {
            Copy-Item -Path $skill.FullName -Destination $commandsDest -Force
            Write-Host "Copied (Claude): $($skill.Name)"
        }
        Write-Host "Done. $($skills.Count) Claude skill(s) installed."
    }
}

# ── PowerShell commands ─────────────────────────────────────────────────────
if (-not $CommandsOnly) {
    $psCommandsSource = Join-Path $repoRoot "ps-commands"

    $loaderBlock = @"

# AI Skills - PowerShell commands loader (added by install.ps1)
# Source: $psCommandsSource
Get-ChildItem -Path '$psCommandsSource' -Filter '*.ps1' -ErrorAction SilentlyContinue |
    ForEach-Object { . `$_.FullName }
"@

    $marker = "AI Skills - PowerShell commands loader"

    if (-not (Test-Path $PROFILE)) {
        New-Item -ItemType File -Path $PROFILE -Force | Out-Null
        Write-Host "Created PowerShell profile at $PROFILE"
    }

    $profileContent = ""
    if (Test-Path $PROFILE) {
        $profileContent = [System.IO.File]::ReadAllText($PROFILE)
    }

    if ($profileContent.Contains($marker)) {
        Write-Host "PowerShell loader already present in $PROFILE"
    } else {
        Add-Content -Path $PROFILE -Value $loaderBlock -Encoding UTF8
        Write-Host "Added PowerShell loader to $PROFILE"
    }

    Write-Host "`nAll done. Restart PowerShell (or run '. `$PROFILE') to load ps-commands."
}
