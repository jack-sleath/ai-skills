function danger-claude {
    Start-Process powershell -ArgumentList '-NoExit', '-Command', 'claude --dangerously-skip-permissions "Ready?"'
    Start-Process powershell -ArgumentList '-NoExit', '-Command', 'claude --dangerously-skip-permissions "/usage"'
}
