function add-repo-children {
    $listFile = Join-Path $HOME ".ps-repo-folders"
    $current = (Get-Location).Path

    $existing = @()
    if (Test-Path $listFile) {
        $existing = Get-Content $listFile | Where-Object { $_ -ne "" }
    }

    $children = Get-ChildItem -Path $current -Directory
    if ($children.Count -eq 0) {
        Write-Host "No subfolders found in $current"
        return
    }

    $added = 0
    foreach ($child in $children) {
        if ($existing -contains $child.FullName) {
            Write-Host "Already in list: $($child.FullName)"
        } else {
            Add-Content -Path $listFile -Value $child.FullName
            Write-Host "Added: $($child.FullName)"
            $added++
        }
    }

    Write-Host "`nDone. $added folder(s) added."
}
