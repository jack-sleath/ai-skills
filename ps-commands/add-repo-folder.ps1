function add-repo-folder {
    $listFile = Join-Path $HOME ".ps-repo-folders"
    $current = (Get-Location).Path

    $existing = @()
    if (Test-Path $listFile) {
        $existing = Get-Content $listFile | Where-Object { $_ -ne "" }
    }

    if ($existing -contains $current) {
        Write-Host "Already in list: $current"
        return
    }

    Add-Content -Path $listFile -Value $current
    Write-Host "Added: $current"
}
