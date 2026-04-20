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

    # Copy role definitions
    $rolesSource = Join-Path $repoRoot "roles"
    $rolesDest = Join-Path $HOME ".claude\roles"

    if (Test-Path $rolesSource) {
        if (-not (Test-Path $rolesDest)) {
            New-Item -ItemType Directory -Path $rolesDest -Force | Out-Null
            Write-Host "Created $rolesDest"
        }

        $roleFiles = Get-ChildItem -Path $rolesSource -Include "*.md","*.json" -File
        foreach ($role in $roleFiles) {
            Copy-Item -Path $role.FullName -Destination $rolesDest -Force
            Write-Host "Copied (Role): $($role.Name)"
        }
        Write-Host "Done. $($roleFiles.Count) role file(s) installed."
    }

    # Seed data files: for JSON arrays-of-named-objects, merge by `name`
    # (live wins on conflict, missing seed entries are appended). For any other
    # shape or non-JSON file, copy only if destination missing.
    $dataSource = Join-Path $repoRoot "data"
    $dataDest = Join-Path $HOME ".claude"
    $mergeScript = Join-Path $repoRoot "scripts\merge_data_json.py"

    if (Test-Path $dataSource) {
        $dataFiles = Get-ChildItem -Path $dataSource -File
        foreach ($dataFile in $dataFiles) {
            $destPath = Join-Path $dataDest $dataFile.Name
            if ($dataFile.Extension -eq ".json" -and (Test-Path $mergeScript)) {
                & python $mergeScript $dataFile.FullName $destPath
            } elseif (Test-Path $destPath) {
                Write-Host "Skipped (Data, exists): $($dataFile.Name)"
            } else {
                Copy-Item -Path $dataFile.FullName -Destination $destPath -Force
                Write-Host "Copied (Data): $($dataFile.Name)"
            }
        }
    }

    # Copy helper scripts
    $scriptsSource = Join-Path $repoRoot "scripts"
    $scriptsDest = Join-Path $HOME ".claude\scripts"

    if (Test-Path $scriptsSource) {
        if (-not (Test-Path $scriptsDest)) {
            New-Item -ItemType Directory -Path $scriptsDest -Force | Out-Null
            Write-Host "Created $scriptsDest"
        }

        $scripts = Get-ChildItem -Path $scriptsSource -Filter "*.py"
        foreach ($script in $scripts) {
            Copy-Item -Path $script.FullName -Destination $scriptsDest -Force
            Write-Host "Copied (Script): $($script.Name)"
        }
        Write-Host "Done. $($scripts.Count) helper script(s) installed."
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
