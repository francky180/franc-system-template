#!/bin/bash
# Perfect Cuts — opens this package's edit in Remotion Studio (Mac).
cd "$(dirname "$0")"
if ! command -v node >/dev/null 2>&1; then
  echo ""
  echo "  Node.js is required (free). Opening the download page..."
  open "https://nodejs.org"
  read -n 1 -s -r -p "  Install Node, then double-click this file again. Press any key to close."
  exit 1
fi
node "_remotion-launcher (C).mjs"
