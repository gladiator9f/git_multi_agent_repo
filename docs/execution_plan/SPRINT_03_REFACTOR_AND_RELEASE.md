# Sprint 3 — Refactor, Package & Release

**Sprint**: Sprint 3 — Merge Conflict Resolution & Shared-File Coordination
**Goal**: Both sessions modify shared files (the hard case), resolve conflicts, and produce a release-ready package
**Duration**: ~10 min
**Sessions**: 2 (Session A + Session B)
**Prerequisite**: Sprint 2 complete (all T07-T12 merged)
**Created**: 2026-08-24

---

## 1. Why This Sprint Exists

Sprints 1-2 kept file ownership isolated. Sprint 3 deliberately creates overlap:
- **T13 + T14 both modify `src/utils/__init__.py`** — forces a merge conflict
- **T15 + T16 both add to `README.md`** — forces coordination on a shared doc
- One session must merge first, the other rebases — demonstrating the conflict resolution protocol

---

## 2. Agent Slots

| Slot | Tasks |
|------|-------|
| **Session A** | T13, T15, T17 |
| **Session B** | T14, T16, T18 |

---

## 3. Task Breakdown

| # | Task | Owner | Files | Conflict Risk | Branch | Status |
|---|------|-------|-------|--------------|--------|--------|
| T13 | Add `__all__` exports + docstring to `src/utils/__init__.py` | Session A | `src/utils/__init__.py` | **HIGH — T14 also edits** | `feature/T13-utils-exports` | 🔴 |
| T14 | Add convenience re-imports to `src/utils/__init__.py` | Session B | `src/utils/__init__.py` | **HIGH — T13 also edits** | `feature/T14-utils-imports` | 🔴 |
| T15 | Add API reference section to README.md | Session A | `README.md` | **MEDIUM — T16 also edits** | `feature/T15-readme-api` | 🔴 |
| T16 | Add contributing guide section to README.md | Session B | `README.md` | **MEDIUM — T15 also edits** | `feature/T16-readme-contributing` | 🔴 |
| T17 | Create `setup.py` / `pyproject.toml` for packaging | Session A | `pyproject.toml` | None | `feature/T17-packaging` | 🔴 |
| T18 | Create `Makefile` with common commands | Session B | `Makefile` | None | `feature/T18-makefile` | 🔴 |

### Conflict Resolution Protocol

**For T13/T14 (`src/utils/__init__.py`):**
1. Session A creates PR for T13 first
2. Session B reviews and merges T13
3. Session B rebases T14 on updated main: `git fetch origin main && git rebase origin/main`
4. Session B resolves any merge conflict in `__init__.py`, ensuring both T13 and T14 changes are present
5. Session B pushes and creates PR for T14

**For T15/T16 (`README.md`):**
Same pattern — whichever PR is created first gets merged first; the other rebases.

---

## 4. Task Specifications

**T13 — Utils Exports** (`src/utils/__init__.py`):
```python
"""Utility functions for string and date manipulation."""

__all__ = [
    "slugify", "truncate", "sanitize_html",
    "format_date", "parse_date", "date_diff_days",
]
```

**T14 — Utils Re-imports** (`src/utils/__init__.py`):
```python
from src.utils.string_helpers import slugify, truncate, sanitize_html
from src.utils.date_helpers import format_date, parse_date, date_diff_days
```
> After conflict resolution, the file should have BOTH the `__all__` and the imports.

**T15 — README API Reference**: Add a section documenting all public functions with signatures.

**T16 — README Contributing**: Add a section explaining the multi-agent PR workflow for contributors.

**T17 — Packaging** (`pyproject.toml`): Standard Python project config with pytest configured.

**T18 — Makefile**:
```makefile
test:       python3 -m pytest tests/ -v
lint:       python3 -m py_compile src/**/*.py
clean:      find . -name __pycache__ -exec rm -rf {} +
```

---

## 5. Execution Timeline

```
Phase 1 (Parallel — CONFLICT ZONE):
  Session A: T13 (utils __all__) → push → create PR
  Session B: T14 (utils imports) → push → create PR
  ⚠️  Both modify src/utils/__init__.py — first PR merged wins, second rebases

Phase 1 Resolution:
  Whichever PR was created first → review → merge
  Other session: git fetch origin main && git rebase origin/main
  Resolve conflict → push --force-with-lease → PR updated

Phase 2 (Parallel — CONFLICT ZONE):
  Session A: T15 (README API) → push → PR
  Session B: T16 (README contributing) → push → PR
  ⚠️  Both modify README.md — same resolution pattern

Phase 3 (Parallel — independent):
  Session A: T17 (pyproject.toml) → push → PR
  Session B: T18 (Makefile) → push → PR
```

---

## 6. Success Criteria

| # | Criterion | How to Verify |
|---|-----------|--------------|
| SC-1 | `src/utils/__init__.py` has BOTH `__all__` AND re-imports | `cat src/utils/__init__.py` |
| SC-2 | At least 1 rebase conflict was resolved | `git log --oneline --all` shows rebase commits |
| SC-3 | README has both API reference and contributing sections | `grep -c "##" README.md` |
| SC-4 | `make test` works | Exit code 0 |
| SC-5 | `pytest tests/` passes on final main | All green |

---

## 7. Session Instructions

### Session A:
```
You are Session A in Sprint 3 (Refactor & Release).

cd /home/ec2-user/environment/my_projects/git_multi_agent_repo
git checkout main && git pull origin main
Read docs/execution_plan/SPRINT_03_REFACTOR_AND_RELEASE.md

Your tasks: T13 (utils exports), T15 (README API ref), T17 (pyproject.toml)
⚠️  T13 and T15 will conflict with Session B's T14 and T16.
If your PR merges first, great. If Session B merges first, you rebase.
```

### Session B:
```
You are Session B in Sprint 3 (Refactor & Release).

cd /home/ec2-user/environment/my_projects/git_multi_agent_repo
git checkout main && git pull origin main
Read docs/execution_plan/SPRINT_03_REFACTOR_AND_RELEASE.md

Your tasks: T14 (utils imports), T16 (README contributing), T18 (Makefile)
⚠️  T14 and T16 will conflict with Session A's T13 and T15.
If your PR merges first, great. If Session A merges first, you rebase.
```

---

**End of Sprint 3 Plan**
