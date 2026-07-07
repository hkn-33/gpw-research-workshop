# CLAUDE.md — project instructions

Follow `AGENTS.md` for the project rules, report naming and tool reference, and `docs/methodology.md` for the research framework.

Claude Code specifics:

- Canonical sources are `skills/` and `agents/` in the repo root; `.claude/commands` and `.claude/agents` are installed copies (`scripts/install-claude.bat` or `.sh`). Edit the sources and reinstall — never the copies.
- Heavier skills delegate to the agents defined in `agents/` (scout, four master lenses, auditor, timing). Launch the four masters in parallel, in a single message.
- Write reports in the language the user communicates in.
- Personal, non-published preferences belong in `CLAUDE.local.md`; the user's positions live in `portfolio.md` (both gitignored).
