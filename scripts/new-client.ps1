# new-client.ps1 — spin up a PRIVATE dashboard repo for a paying client (one command)
# Usage:  pwsh scripts/new-client.ps1 -Client acme  [-Brand "Acme AI"]
param(
  [Parameter(Mandatory=$true)][string]$Client,
  [string]$Brand = ""
)
$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
$src  = Join-Path $root "dashboard"
if (-not (Test-Path $src)) { throw "dashboard/ not found in template root" }

$work = Join-Path $env:TEMP "client-$Client"
if (Test-Path $work) { Remove-Item -Recurse -Force $work }
Copy-Item -Recurse $src $work

# brand it (optional)
if ($Brand -ne "") {
  $env = Join-Path $work ".env.local"
  "NEXT_PUBLIC_APP_NAME=$Brand" | Out-File -FilePath $env -Encoding utf8 -Append
}

Push-Location $work
git init -q
git add .
git -c user.email=setup@local -c user.name=Setup commit -q -m "init $Client dashboard from AI Business Factory template"
# create a PRIVATE repo under your account and push
gh repo create "$Client-dashboard" --private --source=. --remote=origin --push
Pop-Location

Write-Host ""
Write-Host "DONE  ->  private repo '$Client-dashboard' created + pushed." -ForegroundColor Green
Write-Host "Next: client copies .env.example -> .env.local, adds their keys, then deploys to Vercel."
Write-Host "Local path: $work"
