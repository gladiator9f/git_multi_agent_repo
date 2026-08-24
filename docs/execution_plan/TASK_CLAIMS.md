# Task Claims — Multi-Sprint Demo

**Updated**: 2026-08-24

---

## Sprint 1 — Parallel Independent Work

| Task | Description | Claimed By | Branch | PR # | Status |
|------|-------------|-----------|--------|------|--------|
| T01 | String helper functions | Session A | feature/T01-string-helpers | — | 🟡 Claimed |
| T02 | Date helper functions | Session B | feature/T02-date-helpers | — | 🟡 Claimed |
| T03 | Configuration module | Session A | feature/T03-config-settings | — | 🟡 Claimed |
| T04 | Task data model | Session B | feature/T04-task-model | — | 🟡 Claimed |
| T05 | String helper tests | Session A | (bundled with T01) | — | 🟡 Claimed |
| T06 | Date helper tests | Session B | (bundled with T02) | — | 🟡 Claimed |

## Sprint 2 — Cross-Session Dependencies

| Task | Description | Claimed By | Branch | PR # | Depends On | Status |
|------|-------------|-----------|--------|------|-----------|--------|
| T07 | Task validator | — | — | — | — | 🔴 Available |
| T08 | Task reporter (uses validator) | — | — | — | T07 merged | 🔴 Available |
| T09 | Shared interfaces (Protocol) | — | — | — | — | 🔴 Available |
| T10 | Pipeline (implements interfaces) | — | — | — | T09 merged | 🔴 Available |
| T11 | CLI entry point | — | — | — | T07 merged | 🔴 Available |
| T12 | Integration tests | — | — | — | T07+T09+T10 | 🔴 Available |

## Sprint 3 — Merge Conflicts & Shared Files

| Task | Description | Claimed By | Branch | PR # | Conflicts With | Status |
|------|-------------|-----------|--------|------|---------------|--------|
| T13 | Utils `__all__` exports | — | — | — | T14 | 🔴 Available |
| T14 | Utils re-imports | — | — | — | T13 | 🔴 Available |
| T15 | README API reference | — | — | — | T16 | 🔴 Available |
| T16 | README contributing guide | — | — | — | T15 | 🔴 Available |
| T17 | pyproject.toml packaging | — | — | — | — | 🔴 Available |
| T18 | Makefile | — | — | — | — | 🔴 Available |

---

## How to Claim

```bash
git checkout main && git pull origin main
# Edit this file — set your session ID, branch, status to 🟡
git add docs/execution_plan/TASK_CLAIMS.md
git commit -m "claim: T0X — Session [A/B]"
git push origin main
# Then create your feature branch
```
