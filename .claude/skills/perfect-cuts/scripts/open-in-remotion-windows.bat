@echo off
rem Perfect Cuts - opens this package's edit in Remotion Studio (Windows).
cd /d "%~dp0"
where node >nul 2>nul
if errorlevel 1 (
  echo.
  echo   Node.js is required ^(free^). Opening the download page...
  start https://nodejs.org
  echo   Install Node, then double-click this file again.
  pause
  exit /b 1
)
node "_remotion-launcher (C).mjs"
pause
