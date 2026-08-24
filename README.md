# Multi-Agent Git PR Workflow

Template repository for coordinating multiple Claude Code sessions via Git branches and Pull Requests.

## Quick Start

1. Open 2+ terminal tabs in this directory
2. Run `claude` in each tab
3. Tell Session A: "You are Session A — read CLAUDE.md and claim your Sprint 1 tasks"
4. Tell Session B: "You are Session B — read CLAUDE.md and claim your Sprint 1 tasks"
5. Watch them work in parallel, create PRs, and review each other's code

## Structure

- `CLAUDE.md` — Instructions for Claude Code sessions (read first)
- `docs/execution_plan/` — Sprint plans and task tracking
- `sync_github.sh` — Push to GitHub with PAT from AWS SSM
- `src/` — Source code
- `tests/` — Test files

## Applying to Other Repos

Copy `CLAUDE.md`, `sync_github.sh`, and `docs/execution_plan/MULTI_AGENT_PR_EXECUTION_TEMPLATE.md` to any repo.
