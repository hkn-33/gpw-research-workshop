#!/bin/sh
# Install skills and agents into this project's Claude Code configuration.
cd "$(dirname "$0")/.." || exit 1
mkdir -p .claude/commands .claude/agents
cp skills/*.md .claude/commands/
cp agents/*.md .claude/agents/
echo "Installed $(ls skills/*.md | wc -l) skills and $(ls agents/*.md | wc -l) agents into .claude/"
echo "Restart your Claude Code session to pick them up."
