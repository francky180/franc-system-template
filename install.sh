#!/usr/bin/env bash
# AI Software Factory — Universal Installer (Mac / Linux / Termux)
# Usage: curl -fsSL https://raw.githubusercontent.com/francky180/franc-system-template/master/install.sh | bash
set -e

echo ""
echo "╔═══════════════════════════════════════════════╗"
echo "║   AI SOFTWARE FACTORY — UNIVERSAL INSTALLER   ║"
echo "╚═══════════════════════════════════════════════╝"
echo ""

# Detect platform
OS="unknown"
if [ -n "$TERMUX_VERSION" ] || [ -d "/data/data/com.termux" ]; then
  OS="termux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
  OS="mac"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
  OS="linux"
fi

echo "📱 Detected: $OS"
echo ""

install_termux() {
  echo "▶ Installing via Termux (pkg)…"
  pkg upgrade -y
  pkg install -y nodejs-lts git
}

install_mac() {
  echo "▶ Installing via Homebrew…"
  if ! command -v brew >/dev/null 2>&1; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  fi
  brew install node git 2>/dev/null || true
}

install_linux() {
  echo "▶ Installing via apt…"
  sudo apt update
  sudo apt install -y curl git
  if ! command -v node >/dev/null 2>&1; then
    curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
    sudo apt install -y nodejs
  fi
}

case "$OS" in
  termux) install_termux ;;
  mac)    install_mac ;;
  linux)  install_linux ;;
  *)
    echo "❌ Unsupported OS. Please install Node.js + Git manually, then re-run."
    exit 1
    ;;
esac

echo ""
echo "▶ Node: $(node --version)"
echo "▶ Git:  $(git --version)"
echo ""

# Install Claude Code
echo "▶ Installing Claude Code…"
if [ "$OS" = "linux" ]; then
  sudo npm install -g @anthropic-ai/claude-code
else
  npm install -g @anthropic-ai/claude-code
fi

# Clone repo
DEST="$HOME/ai-software-factory"
if [ ! -d "$DEST" ]; then
  echo ""
  echo "▶ Cloning system to $DEST…"
  git clone https://github.com/francky180/franc-system-template.git "$DEST"
fi

cd "$DEST"

# Run installer
if [ -f "ai-tools/install-all.sh" ]; then
  echo ""
  echo "▶ Running install-all.sh (115 skills)…"
  bash ai-tools/install-all.sh
fi

echo ""
echo "╔═══════════════════════════════════════════════╗"
echo "║   ✅ INSTALL COMPLETE                         ║"
echo "║                                               ║"
echo "║   Launching Claude Code…                      ║"
echo "║   Log in with your Claude Max account.        ║"
echo "║   Then type /help to see all 115 skills.      ║"
echo "╚═══════════════════════════════════════════════╝"
echo ""

exec claude
