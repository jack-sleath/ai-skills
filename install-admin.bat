@echo off
cd /d "%~dp0"

git diff --quiet && git diff --cached --quiet
if errorlevel 1 (
    echo.
    echo WARNING: You have uncommitted local changes:
    echo.
    git status --short
    echo.
    echo Pull aborted to avoid overwriting your work.
    echo Commit, stash, or discard these changes before re-running.
    echo.
    pause
    exit /b 1
)

git fetch origin main
git pull
if errorlevel 1 (
    echo.
    echo ERROR: git pull failed.
    pause
    exit /b 1
)

powershell -ExecutionPolicy Bypass -File "%~dp0install.ps1"
