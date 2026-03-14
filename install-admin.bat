@echo off
cd /d "%~dp0"
git pull
powershell -Command "Start-Process powershell -ArgumentList '-ExecutionPolicy Bypass -File ""%~dp0install.ps1""' -Verb RunAs -Wait"
