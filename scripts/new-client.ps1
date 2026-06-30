# new-client.ps1 — spin up a PRIVATE dashboard repo for a paying client (one command)
# The dashboard app lives in the PRIVATE template repo (not public). This clones it
# and creates a fresh private repo for the client.
# Usage:  pwsh scripts/new-client.ps1 -Client acme  [-Brand "Acme AI"]
param(
  [Parameter(Mandatory=$true)][string]$Client,
  [string]$Brand = "",
  [string]$Template = "francky180/asf-dashboard-template"   # PRIVATE source
)
$ErrorActionPreference = "Stop"
$work = Join-Path $env:TEMP "client-$Client"
if (Test-Path $work) { Remove-Item -Recurse -Force $work }

# clone the private dashboard template (requires `gh auth login`)
gh repo clone $Template $work -- --depth 1
Remove-Item -Recurse -Force (Join-Path $work ".git")

if ($Brand -ne "") { "NEXT_PUBLIC_APP_NAME=$Brand" | Out-File (Join-Path $work ".env.local") -Encoding utf8 -Append }

Push-Location $work
git init -q
git add -A; git add -f .env.example 2>$null
git -c user.email=setup@local -c user.name=Setup commit -q -m "init $Client dashboard"
gh repo create "$Client-dashboard" --private --source=. --remote=origin --push
Pop-Location

Write-Host ""
Write-Host "DONE -> private repo '$Client-dashboard' created + pushed." -ForegroundColor Green
Write-Host "Client: copy .env.example -> .env.local, add keys, deploy to Vercel."
