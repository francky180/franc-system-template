#!/bin/bash
# new-client.sh — spin up a PRIVATE dashboard repo for a paying client (one command)
# Usage:  bash scripts/new-client.sh acme  ["Acme AI"]
set -e
CLIENT="$1"; BRAND="${2:-}"
[ -z "$CLIENT" ] && { echo "usage: new-client.sh <client-name> [\"Brand Name\"]"; exit 1; }

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/dashboard"
[ -d "$SRC" ] || { echo "dashboard/ not found in template root"; exit 1; }

WORK="${TMPDIR:-/tmp}/client-$CLIENT"
rm -rf "$WORK"; cp -r "$SRC" "$WORK"

# brand it (optional)
[ -n "$BRAND" ] && echo "NEXT_PUBLIC_APP_NAME=$BRAND" >> "$WORK/.env.local"

cd "$WORK"
git init -q
git add .
git -c user.email=setup@local -c user.name=Setup commit -q -m "init $CLIENT dashboard from AI Business Factory template"
# create a PRIVATE repo under your account and push
gh repo create "$CLIENT-dashboard" --private --source=. --remote=origin --push

echo ""
echo "DONE  ->  private repo '$CLIENT-dashboard' created + pushed."
echo "Next: client copies .env.example -> .env.local, adds their keys, then deploys to Vercel."
echo "Local path: $WORK"
