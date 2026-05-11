#!/usr/bin/env bash
# ============================================================
# AI SOFTWARE FACTORY — One-click install
# Run: bash ai-tools/install-all.sh
# ============================================================

set -e
echo ""
echo "=========================================="
echo "  AI SOFTWARE FACTORY INSTALL"
echo "  115+ Skills in 5 Minutes"
echo "=========================================="
echo ""

BACKUP_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# ----- Step 1: Check prerequisites -----
echo "[1/8] Checking prerequisites..."

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
echo "[2/8] Installing Claude Code..."
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
echo "[3/8] Installing Bun..."
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

# ----- Step 4: Install bundled AI Software Factory skills -----
echo ""
echo "[4/8] Installing bundled AI Software Factory skills..."
BUNDLED_SKILLS_DIR="$BACKUP_DIR/.claude/skills"
TARGET_SKILLS_DIR="$HOME/.claude/skills"
mkdir -p "$TARGET_SKILLS_DIR"
if [ -d "$BUNDLED_SKILLS_DIR" ]; then
  cp -rn "$BUNDLED_SKILLS_DIR"/* "$TARGET_SKILLS_DIR/" 2>/dev/null || true
  BUNDLED_COUNT=$(find "$BUNDLED_SKILLS_DIR" -maxdepth 1 -mindepth 1 -type d | wc -l)
  echo "  Copied $BUNDLED_COUNT bundled skills into $TARGET_SKILLS_DIR"
else
  BUNDLED_COUNT=0
  echo "  (no bundled skills directory found — skipping)"
fi

# ----- Step 5: Install gstack -----
echo ""
echo "[5/8] Installing gstack (35+ specialist skills)..."
if [ -d "$HOME/.claude/skills/gstack" ]; then
  echo "  Already installed. Updating..."
  cd "$HOME/.claude/skills/gstack" && git pull && ./setup
else
  git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git "$HOME/.claude/skills/gstack"
  cd "$HOME/.claude/skills/gstack" && ./setup
fi
echo "  gstack installed."

# ----- Step 6: Install Superpowers -----
echo ""
echo "[6/8] Installing Superpowers (14 process skills)..."
if [ -d "$HOME/.claude/skills/superpowers" ]; then
  echo "  Already installed. Updating..."
  cd "$HOME/.claude/skills/superpowers" && git pull
else
  git clone --single-branch --depth 1 https://github.com/obra/superpowers.git "$HOME/.claude/skills/superpowers"
fi
echo "  Superpowers installed."

# ----- Step 7: Set up BRAIN vault -----
echo ""
echo "[7/8] Setting up BRAIN Obsidian vault..."
BRAIN_DIR="$HOME/BRAIN"
if [ -d "$BRAIN_DIR" ]; then
  echo "  BRAIN already exists. Merging new files only..."
  cp -rn "$BACKUP_DIR/BRAIN/"* "$BRAIN_DIR/" 2>/dev/null || true
else
  cp -r "$BACKUP_DIR/BRAIN" "$BRAIN_DIR"
fi
echo "  BRAIN ready at $BRAIN_DIR"

# ----- Step 8: Set up Claude config -----
echo ""
echo "[8/8] Setting up Claude Code config..."
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
TOTAL=$(find "$HOME/.claude/skills" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | wc -l)
echo "  You now have:"
echo "    - Claude Code CLI"
echo "    - Bun $(bun --version 2>/dev/null || echo 'installed')"
echo "    - ${BUNDLED_COUNT:-114} bundled AI Software Factory skills (copied into ~/.claude/skills/)"
echo "    - gstack (35+ specialist skills) at ~/.claude/skills/gstack/"
echo "    - Superpowers (14 process skills) at ~/.claude/skills/superpowers/"
echo "    - BRAIN Obsidian vault at ~/BRAIN"
echo "    - Total skill folders in ~/.claude/skills/: $TOTAL"
echo "    - CLAUDE.md global identity + skill routing rules"
echo "    - settings.json with PostToolUse auto-sync hook"
echo ""
echo "  Next steps:"
echo "    1. Open Claude Code: type 'claude' in your terminal"
echo "    2. Log in with your Anthropic / Claude Max account"
echo "    3. Type '/help' to see every installed skill"
echo "    4. Open BRAIN in Obsidian: open ~/BRAIN as a vault"
echo "    5. Start your first task: type /office-hours"
echo ""
echo "  Your AI Software Factory is ready."
echo ""
