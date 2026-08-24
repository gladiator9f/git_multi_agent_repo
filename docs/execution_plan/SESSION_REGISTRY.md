# Session Registry — Active Sprint Assignments

**Purpose**: Maps each active session to its assigned sprint and tasks. Replaces the single `CURRENT_SPRINT.md` pointer when sessions work on different sprints simultaneously.

**Updated**: 2026-08-24

---

## How To Use

1. When the operator starts your session, they tell you your **session ID** and **sprint assignment**
2. Find your row below — it tells you which sprint plan to read
3. Read that sprint's execution plan, NOT `CURRENT_SPRINT.md`
4. Before starting work, check `FILE_OWNERSHIP_MATRIX.md` for cross-sprint file collisions

---

## Active Sessions

| Session | Sprint | Execution Plan | Tasks | Worktree Path | Status |
|---------|--------|---------------|-------|---------------|--------|
| Session A | Sprint 1 | `SPRINT_01_SETUP_AND_DEMO.md` | T01, T03, T05 | — | ✅ Complete |
| Session B | Sprint 1 | `SPRINT_01_SETUP_AND_DEMO.md` | T02, T04, T06 | — | ✅ Complete |
| — | Sprint 2 | `SPRINT_02_CROSS_SESSION_COORDINATION.md` | T07-T12 | — | 🔴 Not Started |
| — | Sprint 3 | `SPRINT_03_REFACTOR_AND_RELEASE.md` | T13-T18 | — | 🔴 Not Started |

---

## Cross-Sprint Session Example

When sessions run different sprints in parallel:

| Session | Sprint | Execution Plan | Tasks | Worktree Path | Status |
|---------|--------|---------------|-------|---------------|--------|
| Session A | Sprint 2 | `SPRINT_02_CROSS_SESSION_COORDINATION.md` | T07, T09, T11 | `.../worktrees/session-a` | 🟡 Active |
| Session B | Sprint 3 | `SPRINT_03_REFACTOR_AND_RELEASE.md` | T14, T16, T18 | `.../worktrees/session-b` | 🟡 Active |

**When this happens:**
- Each session reads its own sprint plan (not `CURRENT_SPRINT.md`)
- Both sessions check `FILE_OWNERSHIP_MATRIX.md` before starting any task
- Cross-sprint dependency flags in the matrix must be satisfied (upstream PRs merged)
- The conflict resolution protocol in `FILE_OWNERSHIP_MATRIX.md` applies when both sprints touch the same file

---

## Operator Instructions

### Assigning sessions to the same sprint (default)

```
Session A prompt: "You are Session A — start Sprint 2 tasks T07, T09, T11"
Session B prompt: "You are Session B — start Sprint 2 tasks T08, T10, T12"
```

### Assigning sessions to different sprints

```
Session A prompt: "You are Session A on Sprint 2 — start tasks T07, T09, T11.
  Check FILE_OWNERSHIP_MATRIX.md for cross-sprint file collisions."

Session B prompt: "You are Session B on Sprint 3 — start tasks T14, T16, T18.
  Check FILE_OWNERSHIP_MATRIX.md for cross-sprint file collisions.
  Note: Sprint 3 T13/T14 modify src/utils/__init__.py which Sprint 1 created."
```

### Updating this registry

Each session updates its own row when:
- Starting work (set Status to `🟡 Active`, fill in Worktree Path)
- Completing all assigned tasks (set Status to `✅ Complete`)
- Abandoning a sprint (set Status to `🔴 Abandoned`, note reason)

```bash
# From the main repo directory (not worktree)
git checkout main && git pull origin main
# Edit SESSION_REGISTRY.md
git add docs/execution_plan/SESSION_REGISTRY.md
git commit -m "registry: Session A active on Sprint 2"
git push origin main
```
