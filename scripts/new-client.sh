#!/bin/bash
# new-client.sh — spin up a PRIVATE dashboard repo for a paying client (one command)
# The dashboard app lives in the PRIVATE template repo (not public). This clones it
# and creates a fresh private repo for the client.
# Usage:  bash scripts/new-client.sh acme  ["Acme AI"]
set -e
CLIENT="$1"; BRAND="${2:-}"
TEMPLATE="${TEMPLATE:-francky180/asf-dashboard-template}"   # PRIVATE source
[ -z "$CLIENT" ] && { echo "usage: new-client.sh <client-name> [\"Brand Name\"]"; exit 1; }

WORK="${TMPDIR:-/tmp}/client-$CLIENT"
rm -rf "$WORK"

# clone the private dashboard template (requires `gh auth login`)
gh repo clone "$TEMPLATE" "$WORK" -- --depth 1
rm -rf "$WORK/.git"

[ -n "$BRAND" ] && echo "NEXT_PUBLIC_APP_NAME=$BRAND" >> "$WORK/.env.local"

cd "$WORK"
git init -q
git add -A; git add -f .env.example 2>/dev/null || true
git -c user.email=setup@local -c user.name=Setup commit -q -m "init $CLIENT dashboard"
gh repo create "$CLIENT-dashboard" --private --source=. --remote=origin --push

echo ""
echo "DONE -> private repo '$CLIENT-dashboard' created + pushed."
echo "Client: copy .env.example -> .env.local, add keys, deploy to Vercel."
