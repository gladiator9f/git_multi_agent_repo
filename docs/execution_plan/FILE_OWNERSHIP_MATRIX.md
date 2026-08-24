# File Ownership Matrix — Cross-Sprint Global View

**Purpose**: Any session on any sprint can check this file to see if their target files are contested by active work in another sprint.

**Updated**: 2026-08-24

---

## How To Use

Before starting a task:
1. Find your task's files in the matrix below
2. Check the **Active?** column — if another task is `🟡 In Progress` or `🔴 Planned` on the same file, coordinate
3. If a cross-sprint collision exists, follow the **Cross-Sprint Conflict Protocol** at the bottom

---

## Matrix

| File | Sprint 1 | Sprint 2 | Sprint 3 | Cross-Sprint Risk |
|------|----------|----------|----------|-------------------|
| `src/utils/string_helpers.py` | T01 (A) ✅ | — | — | None |
| `src/utils/date_helpers.py` | T02 (B) ✅ | — | — | None |
| `src/utils/__init__.py` | — | — | T13 (A) + T14 (B) ⚠️ | **Intra-sprint**: T13↔T14 |
| `src/config/settings.py` | T03 (A) ✅ | — | — | None |
| `src/config/__init__.py` | T03 (A) ✅ | — | — | None |
| `src/models/task.py` | T04 (B) ✅ | T07 imports | — | **Read-only in S2**: T07 imports Task model |
| `src/models/__init__.py` | T04 (B) ✅ | — | — | None |
| `tests/test_string_helpers.py` | T05 (A) ✅ | — | — | None |
| `tests/test_date_helpers.py` | T06 (B) ✅ | — | — | None |
| `tests/test_settings.py` | T03 (A) ✅ | — | — | None |
| `tests/test_task_model.py` | T04 (B) ✅ | — | — | None |
| `src/validators/__init__.py` | — | T07 (A) | — | None |
| `src/validators/task_validator.py` | — | T07 (A) | — | None |
| `tests/test_task_validator.py` | — | T07 (A) | — | None |
| `src/reports/__init__.py` | — | T08 (B) | — | None |
| `src/reports/task_reporter.py` | — | T08 (B) | — | **Cross-sprint import**: uses T07's validator |
| `tests/test_task_reporter.py` | — | T08 (B) | — | None |
| `src/interfaces.py` | — | T09 (A) | — | None |
| `tests/test_interfaces.py` | — | T09 (A) | — | None |
| `src/pipeline.py` | — | T10 (B) | — | **Cross-sprint import**: implements T09 interfaces |
| `tests/test_pipeline.py` | — | T10 (B) | — | None |
| `src/cli.py` | — | T11 (A) | — | **Cross-sprint import**: uses T07 + Sprint 1 modules |
| `tests/test_integration.py` | — | T12 (B) | — | **Multi-dep**: T07+T09+T10 must be merged |
| `README.md` | — | — | T15 (A) + T16 (B) ⚠️ | **Intra-sprint**: T15↔T16 |
| `pyproject.toml` | — | — | T17 (A) | None |
| `Makefile` | — | — | T18 (B) | None |

---

## Import Dependency Graph (Cross-Sprint)

```
Sprint 1 (stable — merged)
├── src/models/task.py ← imported by Sprint 2 T07, T08, T12
├── src/utils/string_helpers.py ← imported by Sprint 2 T11
├── src/utils/date_helpers.py
└── src/config/settings.py

Sprint 2 (builds on Sprint 1)
├── src/validators/task_validator.py ← imported by T08, T11, T12
├── src/interfaces.py ← implemented by T10, tested by T12
├── src/reports/task_reporter.py ← tested by T12
├── src/pipeline.py ← tested by T12
└── src/cli.py

Sprint 3 (modifies Sprint 1 files)
├── src/utils/__init__.py ← T13+T14 both write (conflict zone)
└── README.md ← T15+T16 both write (conflict zone)
```

---

## Cross-Sprint Dependency Flags

Tasks that import from code produced by a different sprint. These dependencies mean the upstream sprint's relevant PRs **must be merged** before starting.

| Task | Sprint | Imports From | Upstream Must Be Merged |
|------|--------|-------------|------------------------|
| T07 | S2 | `src/models/task.py` (S1) | S1 T04 ✅ |
| T08 | S2 | `src/validators/task_validator.py` (S2 T07) | S2 T07 |
| T10 | S2 | `src/interfaces.py` (S2 T09) | S2 T09 |
| T11 | S2 | `src/validators/` (S2 T07) + `src/utils/` (S1) | S1 ✅ + S2 T07 |
| T12 | S2 | Everything above | S1 ✅ + S2 T07+T09+T10 |
| T13 | S3 | `src/utils/string_helpers.py` (S1) | S1 ✅ |
| T14 | S3 | `src/utils/date_helpers.py` (S1) | S1 ✅ |

---

## Cross-Sprint Conflict Protocol

When sessions on **different sprints** touch the same file:

1. **Read-only imports are safe** — if your task only `import`s from a file owned by another sprint, no coordination needed (the file is already merged to main)
2. **Write collisions require sequencing** — if both tasks modify the same file:
   - Check `TASK_CLAIMS.md` — is the other task active?
   - If yes: the task that creates a PR **first** gets merged first
   - The other session must `git fetch origin main && git rebase origin/main` and resolve conflicts
   - If the conflict is complex, comment on the PR describing what changed
3. **Interface changes break downstream** — if you modify a file that another sprint imports from (e.g., changing a function signature in Sprint 1 code while Sprint 2 uses it):
   - **Do not modify the public API** of merged code without updating all importers
   - Check the Import Dependency Graph above for downstream consumers
   - Add a deprecation or adapter if the API must change

---

## Keeping This File Current

When adding a new sprint execution plan:
1. Add all new files to the matrix with their task/session assignments
2. Update the Import Dependency Graph if new cross-sprint imports exist
3. Add entries to Cross-Sprint Dependency Flags for any task that imports across sprint boundaries
