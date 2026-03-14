@echo off
cd /d "%~dp0"
git pull
powershell -ExecutionPolicy Bypass -File "%~dp0install.ps1"
