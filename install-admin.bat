@echo off
cd /d "%~dp0"
git pull

:: Update PowerShell profile as current user (not admin)
powershell -ExecutionPolicy Bypass -File "%~dp0install.ps1" -ProfileOnly

:: Create symlinks as admin
powershell -Command "Start-Process powershell -ArgumentList '-ExecutionPolicy Bypass -File ""%~dp0install.ps1"" -SymlinksOnly' -Verb RunAs -Wait"
