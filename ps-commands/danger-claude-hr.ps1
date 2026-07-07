function danger-claude-hr {
    # Like danger-claude, but routes Claude Code through the Headroom
    # context-compression proxy (isolated venv at C:\hr; C:\hr\Scripts on PATH).
    # Bypasses all permission checks, then swaps to auto mode via /auto.
    # Any extra args are forwarded to claude (e.g. danger-claude-hr --resume <id>).
    $hr = (Get-Command headroom -ErrorAction SilentlyContinue).Source
    if (-not $hr) { $hr = 'C:\hr\Scripts\headroom.exe' }
    if (-not (Test-Path $hr)) {
        Write-Error "Headroom not found at '$hr'. Install into the short path C:\hr (e.g. py -m venv C:\hr; C:\hr\Scripts\pip install ""headroom-ai[proxy]""), then keep it updated with 'headroom update'."
        return
    }
    & $hr wrap claude -- --dangerously-skip-permissions @args "/auto"
}
