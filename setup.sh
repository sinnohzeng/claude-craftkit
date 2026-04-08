#!/bin/bash
set -euo pipefail
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$HOME/.claude/skills"
TOOLKIT_DIR="$REPO_DIR/plugins/workflow-toolkit/skills"

mkdir -p "$SKILLS_DIR"

for skill in commit sync-docs ddd review-plan fix-ci save-plan capture-lesson verify-done wrap-up; do
  target="$TOOLKIT_DIR/$skill"
  link="$SKILLS_DIR/$skill"
  if [ -L "$link" ]; then
    rm "$link"
  fi
  ln -sf "$target" "$link"
  echo "✓ $skill → $target"
done

echo ""
echo "Done. 9 skills linked to ~/.claude/skills/"
echo "Run /skills in Claude Code to verify."
