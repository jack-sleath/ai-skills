@echo off
cd /d "%~dp0"
git pull

:: Update PowerShell profile as current user (not admin)
powershell -ExecutionPolicy Bypass -File "%~dp0install.ps1" -ProfileOnly

:: Create symlinks as admin, passing the real user's home so paths resolve correctly
powershell -Command "Start-Process powershell -ArgumentList '-ExecutionPolicy Bypass -File ""%~dp0install.ps1"" -SymlinksOnly -UserHome ''%USERPROFILE%''' -Verb RunAs -Wait"
