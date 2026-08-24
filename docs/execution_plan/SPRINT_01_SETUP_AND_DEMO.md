# Sprint 1 — Setup & Demo

**Sprint**: Sprint 1 — Multi-Agent PR Workflow Demo
**Goal**: Demonstrate parallel feature development across 2 Claude Code sessions with PR-based review
**Duration**: 1 session (~30 min)
**Sessions**: 2 (Session A + Session B)
**Created**: 2026-08-24

---

## 1. Executive Summary

| Dimension | Detail |
|-----------|--------|
| **Sprint Goal** | Build utility modules in parallel across 2 sessions, create PRs, cross-review, and merge |
| **Tasks** | 6 tasks across 2 agent slots |
| **Files Created** | 6 Python files (3 source + 3 test) |
| **PRs Expected** | 4 PRs (T01, T02, T03+T05, T04+T06) |
| **Dependencies** | T05 depends on T01; T06 depends on T02 |

---

## 2. Agent Slots

| Slot | Session | Primary Focus | Tasks |
|------|---------|---------------|-------|
| **Session A** | Claude Code terminal #1 | String utilities + config | T01, T03, T05 |
| **Session B** | Claude Code terminal #2 | Date utilities + models | T02, T04, T06 |

---

## 3. Task Breakdown

| # | Task | Owner | Priority | Files Touched | Dependencies | Branch | Status |
|---|------|-------|----------|---------------|--------------|--------|--------|
| T01 | Create string helper functions | Session A | P0 | `src/utils/string_helpers.py` | None | `feature/T01-string-helpers` | 🔴 Not Started |
| T02 | Create date helper functions | Session B | P0 | `src/utils/date_helpers.py` | None | `feature/T02-date-helpers` | 🔴 Not Started |
| T03 | Create configuration module | Session A | P0 | `src/config/settings.py` | None | `feature/T03-config-settings` | 🔴 Not Started |
| T04 | Create Task data model | Session B | P0 | `src/models/task.py` | None | `feature/T04-task-model` | 🔴 Not Started |
| T05 | Tests for string helpers | Session A | P1 | `tests/test_string_helpers.py` | T01 merged | `feature/T05-test-string-helpers` | 🔴 Not Started |
| T06 | Tests for date helpers | Session B | P1 | `tests/test_date_helpers.py` | T02 merged | `feature/T06-test-date-helpers` | 🔴 Not Started |

### Task Specifications

**T01 — String Helpers** (`src/utils/string_helpers.py`):
- `slugify(text: str) -> str` — Convert text to URL-safe slug
- `truncate(text: str, max_length: int = 100, suffix: str = "...") -> str` — Truncate with suffix
- `sanitize_html(text: str) -> str` — Strip HTML tags from text

**T02 — Date Helpers** (`src/utils/date_helpers.py`):
- `format_date(dt: datetime, fmt: str = "%Y-%m-%d") -> str` — Format datetime to string
- `parse_date(date_str: str, fmt: str = "%Y-%m-%d") -> datetime` — Parse string to datetime
- `date_diff_days(start: datetime, end: datetime) -> int` — Calculate day difference

**T03 — Configuration** (`src/config/settings.py`):
- `Settings` dataclass with `debug`, `log_level`, `app_name`, `version` fields
- `load_settings() -> Settings` — Load from environment variables with defaults

**T04 — Task Model** (`src/models/task.py`):
- `TaskStatus` enum: `TODO`, `IN_PROGRESS`, `IN_REVIEW`, `DONE`
- `Task` dataclass with `id`, `title`, `description`, `status`, `assignee`, `branch`, `pr_url`, `created_at`
- `create_task(title, description, assignee) -> Task` — Factory function

**T05 — String Helper Tests** (`tests/test_string_helpers.py`):
- Test `slugify` with spaces, special chars, unicode
- Test `truncate` with short text, exact length, long text
- Test `sanitize_html` with tags, nested tags, no tags

**T06 — Date Helper Tests** (`tests/test_date_helpers.py`):
- Test `format_date` with default and custom format
- Test `parse_date` with valid and invalid input
- Test `date_diff_days` with positive, negative, same-day

---

## 4. File Ownership Matrix

| File | Owner Task | Owner Session |
|------|------------|---------------|
| `src/utils/string_helpers.py` | T01 | Session A |
| `src/utils/date_helpers.py` | T02 | Session B |
| `src/config/settings.py` | T03 | Session A |
| `src/models/task.py` | T04 | Session B |
| `tests/test_string_helpers.py` | T05 | Session A |
| `tests/test_date_helpers.py` | T06 | Session B |

---

## 5. Parallel Execution Timeline

```
Phase 1 (Parallel — no dependencies):
  Session A: T01 (string helpers)     →  PR #1
  Session B: T02 (date helpers)       →  PR #2

Phase 1b (Parallel — no dependencies):
  Session A: T03 (config)             →  PR #3 (can bundle with T01 or separate)
  Session B: T04 (task model)         →  PR #4 (can bundle with T02 or separate)

Phase 2 (After Phase 1 PRs merged):
  Session A: T05 (string tests)       →  PR #5 (or bundle with T01 PR)
  Session B: T06 (date tests)         →  PR #6 (or bundle with T02 PR)
```

**Simplification**: Sessions MAY bundle T01+T05 and T02+T06 into single PRs if they prefer (code + tests together is natural). The separation exists to demonstrate the dependency tracking pattern.

---

## 6. PR Review Assignment

| PR | Author | Reviewer | Scope |
|----|--------|----------|-------|
| T01 (string helpers) | Session A | Session B | Code quality, edge cases |
| T02 (date helpers) | Session B | Session A | Code quality, edge cases |
| T03 (config) | Session A | Session B | Defaults reasonable, env var naming |
| T04 (task model) | Session B | Session A | Dataclass correctness, enum values |

---

## 7. Success Criteria

| # | Criterion | Verification |
|---|-----------|-------------|
| SC-1 | All 6 files created | `find src tests -name "*.py" -not -name "__init__.py" | wc -l` = 6 |
| SC-2 | All tests pass | `pytest tests/ -v` exits 0 |
| SC-3 | At least 2 PRs created | `gh pr list --state all` shows ≥2 |
| SC-4 | At least 1 cross-session review | PR has a review comment from the non-author session |
| SC-5 | No merge conflicts | Clean merge history on main |
| SC-6 | TASK_CLAIMS.md fully updated | All tasks show ✅ |

---

## 8. Sprint Closing

| # | Task | Owner | Status |
|---|------|-------|--------|
| C1 | All PRs merged to main | Both | 🔴 |
| C2 | `pytest tests/` passes on main | Either | 🔴 |
| C3 | TASK_CLAIMS.md all ✅ | Lead | 🔴 |
| C4 | Final push to GitHub | Operator | 🔴 |

---

**End of Sprint 1 Plan**
