# Multi-Agent PR Execution Plan Template

**Sprint**: [Sprint N — Sprint Name]
**Goal**: [One-sentence sprint goal]
**Duration**: [N days/weeks]
**Sessions**: [Number of concurrent Claude Code sessions]
**Template Version**: 1.0.0
**Forked From**: Doscierge Agent Teams Execution Plan Template v1.4.0 (simplified for PR-based multi-session work)

---

## 1. Executive Summary

| Dimension | Detail |
|-----------|--------|
| **Sprint Goal** | [One sentence] |
| **Tasks** | [N tasks across M agent slots] |
| **Files Created/Modified** | [List key files] |
| **PRs Expected** | [N PRs, one per task] |
| **Dependencies** | [Which tasks depend on others] |

---

## 2. Agent Slots

Each agent slot maps to a Claude Code session running simultaneously.

| Slot | Session | Primary Focus | Tasks |
|------|---------|---------------|-------|
| **Session A** | Claude Code terminal #1 | [Focus area] | T01, T03, T05 |
| **Session B** | Claude Code terminal #2 | [Focus area] | T02, T04, T06 |

> **Slot assignment**: The operator tells each session which slot it is at sprint start. The session then claims its assigned tasks in `TASK_CLAIMS.md`.

---

## 3. Task Breakdown

| # | Task | Owner | Priority | Files Touched | Dependencies | Branch | Status |
|---|------|-------|----------|---------------|--------------|--------|--------|
| T01 | [Task description] | Session A | P0 | `src/path/file.py` | None | `feature/T01-desc` | 🔴 Not Started |
| T02 | [Task description] | Session B | P0 | `src/path/other.py` | None | `feature/T02-desc` | 🔴 Not Started |

### Task Status Legend

| Icon | Status |
|------|--------|
| 🔴 | Not Started |
| 🟡 | Claimed (in TASK_CLAIMS.md) |
| 🔄 | In Progress (branch created, work underway) |
| 🟢 | PR Created |
| ✅ | Merged |
| ❌ | Blocked / Abandoned |

---

## 4. File Ownership Matrix

**CRITICAL**: Each file belongs to EXACTLY ONE task. No two tasks modify the same file.

| File Pattern | Owner Task | Owner Session | Notes |
|-------------|------------|---------------|-------|
| `src/utils/string_helpers.py` | T01 | Session A | New file |
| `src/utils/date_helpers.py` | T02 | Session B | New file |
| `tests/test_string_helpers.py` | T05 | Session A | Tests for T01 |
| `tests/test_date_helpers.py` | T06 | Session B | Tests for T02 |

> If two tasks MUST touch the same file, they must be sequenced (one merges first, the other rebases).

---

## 5. Parallel Execution Timeline

```
Phase 1 (Parallel — no dependencies):
  Session A: T01 (feature code)     | Session B: T02 (feature code)
  Session A: T03 (config)           | Session B: T04 (models)

Phase 2 (Parallel — depends on Phase 1 merge):
  Session A: T05 (tests for T01)    | Session B: T06 (tests for T02)
```

| Tasks | Relationship | Rationale |
|-------|-------------|-----------|
| T01, T02 | **Parallel** | No shared files |
| T05 → T01 | **Sequential** | Tests need the code to exist |
| T03, T04 | **Parallel** | No shared files |

---

## 6. Branch Strategy

| Task | Branch Name | Base | Merge Target |
|------|------------|------|--------------|
| T01 | `feature/T01-desc` | main | main (via PR) |
| T02 | `feature/T02-desc` | main | main (via PR) |

### Merge Order (if dependencies exist)

1. T01 and T02 can merge in any order (no conflict)
2. T05 merges after T01
3. T06 merges after T02

---

## 7. PR Review Assignment

| PR (Task) | Author Session | Reviewer Session | Review Criteria |
|-----------|---------------|-----------------|-----------------|
| T01 PR | Session A | Session B | Code quality, tests pass |
| T02 PR | Session B | Session A | Code quality, tests pass |

### Review Checklist (for reviewer)

- [ ] Code runs without errors
- [ ] Tests pass (`pytest tests/`)
- [ ] Conventional commit messages
- [ ] No files outside task scope modified
- [ ] No hardcoded secrets or credentials

---

## 8. Success Criteria

| # | Criterion | Verification |
|---|-----------|-------------|
| SC-1 | All tasks completed and merged | `git log --oneline main` shows all task commits |
| SC-2 | All tests pass | `pytest tests/` exits 0 |
| SC-3 | No merge conflicts | Clean merge history |
| SC-4 | TASK_CLAIMS.md fully updated | All tasks show ✅ |

---

## 9. Conflict Resolution Protocol

| Scenario | Resolution |
|----------|-----------|
| Two PRs touch the same file | Merge the one with fewer changes first; other session rebases |
| PR review finds issues | Reviewer comments on PR; author fixes and re-pushes |
| Task dependency not met | Dependent task waits; author works on another available task |
| Session crashes mid-task | Other session can pick up the branch and continue |

---

## 10. Sprint Closing Tasks

| # | Task | Owner | Status |
|---|------|-------|--------|
| C1 | All PRs merged to main | Both sessions | 🔴 |
| C2 | All tests pass on main | Either session | 🔴 |
| C3 | TASK_CLAIMS.md updated (all ✅) | Lead session | 🔴 |
| C4 | Push final main to GitHub | Operator or session | 🔴 |
| C5 | Archive sprint plan to `completed/` | Lead session | 🔴 |

---

**End of Template**

*One task per branch. One PR per task. File ownership prevents conflicts. Sessions coordinate through TASK_CLAIMS.md and PR reviews.*
