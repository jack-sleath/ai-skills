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

    # Build display names
    $names = $folders | ForEach-Object { Split-Path $_ -Leaf }

    $filter = ""
    $selectedIndex = 0

    function Get-Filtered {
        param($f)
        $result = @()
        for ($i = 0; $i -lt $names.Count; $i++) {
            if ($f -eq "" -or $names[$i] -like "*$f*") {
                $result += $i
            }
        }
        return $result
    }

    function Render {
        param($filter, $selectedIndex, $filteredIndices, $lineCount)

        # Move cursor up to overwrite previous render
        if ($lineCount -gt 0) {
            $newTop = [Console]::CursorTop - $lineCount
            if ($newTop -lt 0) { $newTop = 0 }
            [Console]::SetCursorPosition(0, $newTop)
        }

        $lines = 0

        # Filter prompt line
        $promptLine = "> $filter"
        Write-Host $promptLine -NoNewline
        # Clear rest of line
        $padding = [Console]::WindowWidth - $promptLine.Length
        if ($padding -gt 0) { Write-Host (" " * $padding) -NoNewline }
        Write-Host ""
        $lines++

        for ($j = 0; $j -lt $filteredIndices.Count; $j++) {
            $idx = $filteredIndices[$j]
            $name = $names[$idx]
            if ($j -eq $selectedIndex) {
                Write-Host "  > $name" -ForegroundColor Cyan -NoNewline
            } else {
                Write-Host "    $name" -NoNewline
            }
            $padding = [Console]::WindowWidth - $name.Length - 4
            if ($padding -gt 0) { Write-Host (" " * $padding) -NoNewline }
            Write-Host ""
            $lines++
        }

        # Clear any leftover lines from previous longer list
        $blank = " " * [Console]::WindowWidth
        for ($j = $filteredIndices.Count; $j -lt $names.Count; $j++) {
            Write-Host $blank
            $lines++
        }

        return $lines
    }

    # Initial render
    $filteredIndices = @(Get-Filtered $filter)
    $totalLines = Render $filter $selectedIndex $filteredIndices 0

    while ($true) {
        $key = [Console]::ReadKey($true)

        if ($key.Key -eq "Enter") {
            if ($filteredIndices.Count -gt 0) {
                $target = $folders[$filteredIndices[$selectedIndex]]
                Write-Host ""
                Set-Location $target
                Write-Host "-> $target"
            } else {
                Write-Host "`nNo match."
            }
            return
        }

        if ($key.Key -eq "Escape") {
            Write-Host "`nCancelled."
            return
        }

        if ($key.Key -eq "UpArrow") {
            if ($selectedIndex -gt 0) { $selectedIndex-- }
        } elseif ($key.Key -eq "DownArrow") {
            if ($selectedIndex -lt $filteredIndices.Count - 1) { $selectedIndex++ }
        } elseif ($key.Key -eq "Backspace") {
            if ($filter.Length -gt 0) {
                $filter = $filter.Substring(0, $filter.Length - 1)
                $filteredIndices = @(Get-Filtered $filter)
                $selectedIndex = 0
            }
        } else {
            $ch = $key.KeyChar
            if ($ch -and [char]::IsLetterOrDigit($ch) -or $ch -eq '-' -or $ch -eq '_' -or $ch -eq '.' -or $ch -eq ' ') {
                $filter += $ch
                $filteredIndices = @(Get-Filtered $filter)
                $selectedIndex = 0
            }
        }

        $totalLines = Render $filter $selectedIndex $filteredIndices $totalLines
    }
}