function goto-repo {
    $listFile = Join-Path $HOME ".ps-repo-folders"

    if (-not (Test-Path $listFile)) {
        Write-Host "No repos saved yet. Use add-repo-folder to add one."
        return
    }

    $allFolders = Get-Content $listFile | Where-Object { $_ -ne "" }
    $folders = $allFolders | Where-Object { Test-Path $_ } | Sort-Object { Split-Path $_ -Leaf }

    $removed = $allFolders | Where-Object { -not (Test-Path $_) }
    if ($removed.Count -gt 0) {
        $folders | Set-Content $listFile
        foreach ($r in $removed) {
            Write-Host "Removed missing path: $r"
        }
    }

    if ($folders.Count -eq 0) {
        Write-Host "No repos saved yet. Use add-repo-folder to add one."
        return
    }

    for ($i = 0; $i -lt $folders.Count; $i++) {
        Write-Host "  [$($i + 1)] $(Split-Path $folders[$i] -Leaf)"
    }

    $input = Read-Host "`nEnter number"

    if ($input -notmatch '^\d+$') {
        Write-Host "Cancelled."
        return
    }

    $index = [int]$input - 1

    if ($index -lt 0 -or $index -ge $folders.Count) {
        Write-Host "Invalid selection."
        return
    }

    $target = $folders[$index]

    Set-Location $target
    Write-Host "-> $target"
}
