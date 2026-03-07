@echo off
title Plotline Installer
cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -File "%~dp0scripts\install.ps1"
echo.
echo Press any key to close...
pause >nul
