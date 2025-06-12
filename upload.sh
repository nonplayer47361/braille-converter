#!/usr/bin/env bash
# upload.sh — Initialize (if needed), commit, and push your project to GitHub in one go.
# Usage: ./upload.sh "Your commit message"

set -euo pipefail

# --- CONFIGURATION ---
# Default branch name
MAIN_BRANCH="main"

# Get commit message from first argument, or use a default
COMMIT_MSG="${1:-"Update code"}"

# Check for git repository; initialize if missing
if [ ! -d .git ]; then
  echo "🔧 Initializing new git repository..."
  git init
  git branch -M "$MAIN_BRANCH"
fi

# Stage all changes
echo "📝 Staging all changes..."
git add .

# Commit
echo "💾 Committing with message: $COMMIT_MSG"
# If there's nothing to commit, skip
if git diff --cached --quiet; then
  echo "⚠️  No changes to commit."
else
  git commit -m "$COMMIT_MSG"
fi

# Check if 'origin' remote exists
if git remote get-url origin >/dev/null 2>&1; then
  echo "🌐 'origin' remote found: $(git remote get-url origin)"
else
  # Try to create repo with GitHub CLI if available
  if command -v gh >/dev/null 2>&1; then
    echo "🚀 Creating GitHub repo and setting 'origin' via gh CLI..."
    gh repo create --public --source . --remote origin --push
    exit 0
  else
    # Ask user for remote URL
    read -p "Enter GitHub remote URL (e.g. git@github.com:user/repo.git): " REMOTE_URL
    git remote add origin "$REMOTE_URL"
  fi
fi

# Push to origin
echo "📤 Pushing to origin/$MAIN_BRANCH..."
git push -u origin "$MAIN_BRANCH"

echo "✅ Done!"