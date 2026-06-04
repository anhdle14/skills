#!/usr/bin/env sh
# bootstrap.sh — one-liner setup for any machine
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/anhdle14/skills/main/bootstrap.sh | sh
#
set -eu

REPO_DIR="$HOME/Developer/github.com/anhdle14/skills"
REPO_URL="https://github.com/anhdle14/skills.git"

# --- Deno ---
if ! command -v deno >/dev/null 2>&1; then
  echo "Installing Deno..."
  curl -fsSL https://deno.land/install.sh | sh
  # Add to PATH for this session
  export DENO_INSTALL="$HOME/.deno"
  export PATH="$DENO_INSTALL/bin:$PATH"
fi

# --- Clone or update repo ---
if [ -d "$REPO_DIR/.git" ]; then
  echo "Updating existing repo at $REPO_DIR..."
  git -C "$REPO_DIR" pull --ff-only
else
  echo "Cloning skills repo to $REPO_DIR..."
  mkdir -p "$(dirname "$REPO_DIR")"
  git clone "$REPO_URL" "$REPO_DIR"
fi

# --- Install (symlink) ---
echo "Linking skills..."
deno run --allow-read --allow-write --allow-env=HOME "$REPO_DIR/install.ts"

echo ""
echo "Done. Skills are now available in ~/.claude/skills and ~/.agents/skills."
echo "Re-run this script anytime to pull updates."
