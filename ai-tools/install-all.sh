#!/usr/bin/env bash
# ============================================================
# AI SOFTWARE FACTORY — One-click install
# Run: bash ai-tools/install-all.sh
# ============================================================

set -e
echo ""
echo "=========================================="
echo "  AI SOFTWARE FACTORY INSTALL"
echo "  102+ Skills in 5 Minutes"
echo "=========================================="
echo ""

BACKUP_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# ----- Step 1: Check prerequisites -----
echo "[1/7] Checking prerequisites..."

if ! command -v node &>/dev/null; then
  echo "ERROR: Node.js not found. Install from https://nodejs.org/"
  exit 1
fi
echo "  Node.js: $(node --version)"

if ! command -v git &>/dev/null; then
  echo "ERROR: Git not found. Install from https://git-scm.com/"
  exit 1
fi
echo "  Git: $(git --version)"

# ----- Step 2: Install Claude Code -----
echo ""
echo "[2/7] Installing Claude Code..."
if command -v claude &>/dev/null; then
  echo "  Already installed: $(claude --version 2>/dev/null || echo 'present')"
else
  echo "  Installing Claude Code..."
  if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    curl -fsSL https://claude.ai/install.cmd -o /tmp/install-claude.cmd && cmd.exe /c /tmp/install-claude.cmd
  else
    curl -fsSL https://claude.ai/install.sh | bash
  fi
fi

# ----- Step 3: Install Bun -----
echo ""
echo "[3/7] Installing Bun..."
if command -v bun &>/dev/null; then
  echo "  Already installed: bun $(bun --version)"
else
  if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    powershell -c "irm bun.sh/install.ps1 | iex"
  else
    curl -fsSL https://bun.sh/install | bash
  fi
  export PATH="$HOME/.bun/bin:$PATH"
  echo "  Installed: bun $(bun --version 2>/dev/null || echo 'done')"
fi
export PATH="$HOME/.bun/bin:$PATH"

# ----- Step 4: Install gstack -----
echo ""
echo "[4/7] Installing gstack (35+ specialist skills)..."
if [ -d "$HOME/.claude/skills/gstack" ]; then
  echo "  Already installed. Updating..."
  cd "$HOME/.claude/skills/gstack" && git pull && ./setup
else
  git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git "$HOME/.claude/skills/gstack"
  cd "$HOME/.claude/skills/gstack" && ./setup
fi
echo "  gstack installed."

# ----- Step 5: Install Superpowers -----
echo ""
echo "[5/7] Installing Superpowers (14 process skills)..."
if [ -d "$HOME/.claude/skills/superpowers" ]; then
  echo "  Already installed. Updating..."
  cd "$HOME/.claude/skills/superpowers" && git pull
else
  git clone --single-branch --depth 1 https://github.com/obra/superpowers.git "$HOME/.claude/skills/superpowers"
fi
echo "  Superpowers installed."

# ----- Step 6: Set up BRAIN vault -----
echo ""
echo "[6/7] Setting up BRAIN Obsidian vault..."
BRAIN_DIR="$HOME/BRAIN"
if [ -d "$BRAIN_DIR" ]; then
  echo "  BRAIN already exists. Merging new files only..."
  cp -rn "$BACKUP_DIR/BRAIN/"* "$BRAIN_DIR/" 2>/dev/null || true
else
  cp -r "$BACKUP_DIR/BRAIN" "$BRAIN_DIR"
fi
echo "  BRAIN ready at $BRAIN_DIR"

# ----- Step 7: Set up Claude config -----
echo ""
echo "[7/7] Setting up Claude Code config..."
CLAUDE_DIR="$HOME/.claude"
mkdir -p "$CLAUDE_DIR"

# CLAUDE.md with gstack routing
if [ ! -f "$HOME/CLAUDE.md" ]; then
  cp "$BACKUP_DIR/claude-config/CLAUDE.md" "$HOME/CLAUDE.md"
  echo "  CLAUDE.md created with skill routing rules."
else
  echo "  CLAUDE.md already exists. Skipping."
fi

# Settings
if [ ! -f "$CLAUDE_DIR/settings.json" ]; then
  cp "$BACKUP_DIR/claude-config/settings.json" "$CLAUDE_DIR/settings.json"
  echo "  Settings copied."
else
  echo "  Settings already exist. Skipping."
fi

echo ""
echo "=========================================="
echo "  INSTALL COMPLETE"
echo "=========================================="
echo ""
echo "  Installed:"
echo "    - Claude Code"
echo "    - Bun $(bun --version 2>/dev/null || echo '')"
echo "    - gstack (35+ specialist skills)"
echo "    - Superpowers (14 process skills)"
echo "    - BRAIN Obsidian vault at ~/BRAIN"
echo "    - CLAUDE.md with routing rules"
echo ""
echo "  Next steps:"
echo "    1. Open Claude Code: type 'claude' in terminal"
echo "    2. Log in with your Anthropic account"
echo "    3. Open BRAIN in Obsidian: ~/BRAIN"
echo "    4. Edit BRAIN/core/MASTER_PROMPT.md with your info"
echo "    5. Start building: type /office-hours"
echo ""
echo "  Your AI Software Factory is ready."
echo ""
