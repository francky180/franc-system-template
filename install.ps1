# AI Software Factory — Universal Installer (Windows)
# Usage: iwr https://raw.githubusercontent.com/francky180/franc-system-template/master/install.ps1 | iex

$ErrorActionPreference = 'Stop'

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════╗" -ForegroundColor Yellow
Write-Host "║   AI SOFTWARE FACTORY — WINDOWS INSTALLER     ║" -ForegroundColor Yellow
Write-Host "╚═══════════════════════════════════════════════╝" -ForegroundColor Yellow
Write-Host ""

# Check admin
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]"Administrator")) {
    Write-Host "❌ Please run PowerShell as Administrator." -ForegroundColor Red
    exit 1
}

Write-Host "▶ Installing Node.js LTS…" -ForegroundColor Cyan
winget install OpenJS.NodeJS.LTS -e --accept-source-agreements --accept-package-agreements --silent 2>$null

Write-Host "▶ Installing Git…" -ForegroundColor Cyan
winget install Git.Git -e --accept-source-agreements --accept-package-agreements --silent 2>$null

# Refresh PATH
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

Write-Host ""
Write-Host "▶ Node: $(node --version 2>$null)" -ForegroundColor Green
Write-Host "▶ Git:  $(git --version 2>$null)" -ForegroundColor Green
Write-Host ""

Write-Host "▶ Installing Claude Code…" -ForegroundColor Cyan
npm install -g @anthropic-ai/claude-code

$dest = "$HOME\ai-software-factory"
if (-Not (Test-Path $dest)) {
    Write-Host ""
    Write-Host "▶ Cloning system to $dest…" -ForegroundColor Cyan
    git clone https://github.com/francky180/franc-system-template.git $dest
}

Set-Location $dest

if (Test-Path "ai-tools\install-all.sh") {
    Write-Host ""
    Write-Host "▶ Running install-all.sh (115 skills)…" -ForegroundColor Cyan
    bash ai-tools/install-all.sh
}

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║   ✅ INSTALL COMPLETE                         ║" -ForegroundColor Green
Write-Host "║                                               ║" -ForegroundColor Green
Write-Host "║   Launching Claude Code…                      ║" -ForegroundColor Green
Write-Host "║   Log in with your Claude Max account.        ║" -ForegroundColor Green
Write-Host "║   Then type /help to see all 115 skills.      ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

claude
