# Sprint 2 — Cross-Session Coordination Demo

**Sprint**: Sprint 2 — Forced Cross-Session Dependencies
**Goal**: Demonstrate dependency chains, PR reviews, and merge-order coordination between 2 Claude Code sessions
**Duration**: ~15 min
**Sessions**: 2 (Session A + Session B)
**Prerequisite**: Sprint 1 PRs merged to main
**Created**: 2026-08-24

---

## 1. Why This Sprint Exists

Sprint 1 showed **parallel independent work** — no conflicts possible. Sprint 2 forces the hard patterns:
- **T07→T08 dependency**: Session B must wait for Session A's PR to merge before starting
- **T09↔T10 shared interface**: Both sessions implement against a shared contract — tests must pass together
- **Cross-review mandatory**: Each session reviews the other's PR before merge

---

## 2. Agent Slots

| Slot | Tasks | Role |
|------|-------|------|
| **Session A** | T07, T09, T11 | Builds the validator + CLI entry point |
| **Session B** | T08, T10, T12 | Builds the reporter (depends on T07) + integration tests |

---

## 3. Task Breakdown

| # | Task | Owner | Files | Dependencies | Branch | Status |
|---|------|-------|-------|-------------|--------|--------|
| T07 | Create task validator | Session A | `src/validators/task_validator.py` | None | `feature/T07-task-validator` | 🔴 |
| T08 | Create task reporter (uses validator) | Session B | `src/reports/task_reporter.py` | **T07 merged** | `feature/T08-task-reporter` | 🔴 |
| T09 | Create shared interfaces module | Session A | `src/interfaces.py` | None | `feature/T09-interfaces` | 🔴 |
| T10 | Implement pipeline using interfaces | Session B | `src/pipeline.py` | **T09 merged** | `feature/T10-pipeline` | 🔴 |
| T11 | Create CLI entry point | Session A | `src/cli.py` | T07 merged | `feature/T11-cli` | 🔴 |
| T12 | Integration tests (all modules) | Session B | `tests/test_integration.py` | **T07+T09+T10 merged** | `feature/T12-integration-tests` | 🔴 |

### Task Specifications

**T07 — Task Validator** (`src/validators/task_validator.py`):
```python
# Validates Task objects from src/models/task.py (Sprint 1)
# validate_task(task: Task) -> list[str]  — returns list of validation errors
# validate_title(title: str) -> str | None  — returns error or None
# validate_assignee(assignee: str, valid_assignees: list[str]) -> str | None
```

**T08 — Task Reporter** (`src/reports/task_reporter.py`) — **DEPENDS ON T07**:
```python
# Uses task_validator to validate before reporting
# generate_report(tasks: list[Task]) -> str  — markdown summary
# generate_status_summary(tasks: list[Task]) -> dict  — counts by status
# Must import and call validate_task() from T07
```

**T09 — Shared Interfaces** (`src/interfaces.py`):
```python
# Protocol classes that T10 implements
# class Processor(Protocol): def process(self, data: dict) -> dict
# class Filter(Protocol): def matches(self, item: dict) -> bool
# class Formatter(Protocol): def format(self, data: dict) -> str
```

**T10 — Pipeline** (`src/pipeline.py`) — **DEPENDS ON T09**:
```python
# Implements the interfaces from T09
# class TaskProcessor(Processor): processes task dicts
# class StatusFilter(Filter): filters by task status
# class MarkdownFormatter(Formatter): formats tasks as markdown
# run_pipeline(tasks, processor, filter, formatter) -> str
```

**T11 — CLI** (`src/cli.py`):
```python
# Simple argparse CLI that ties modules together
# Commands: validate, report, pipeline
# Uses task_validator (T07), string_helpers (Sprint 1)
```

**T12 — Integration Tests** (`tests/test_integration.py`) — **DEPENDS ON T07+T09+T10**:
```python
# Tests that cross module boundaries
# test_validator_with_real_tasks
# test_reporter_uses_validator
# test_pipeline_end_to_end
# test_cli_commands (subprocess)
```

---

## 4. File Ownership

| File | Task | Session |
|------|------|---------|
| `src/validators/__init__.py` | T07 | A |
| `src/validators/task_validator.py` | T07 | A |
| `tests/test_task_validator.py` | T07 | A |
| `src/reports/__init__.py` | T08 | B |
| `src/reports/task_reporter.py` | T08 | B |
| `tests/test_task_reporter.py` | T08 | B |
| `src/interfaces.py` | T09 | A |
| `tests/test_interfaces.py` | T09 | A |
| `src/pipeline.py` | T10 | B |
| `tests/test_pipeline.py` | T10 | B |
| `src/cli.py` | T11 | A |
| `tests/test_integration.py` | T12 | B |

---

## 5. Execution Timeline — Forced Coordination

```
Phase 1 (Parallel — independent):
  Session A: T07 (validator) → push → create PR
  Session B: (waits or works on T09 review prep)

Phase 1b (Parallel — independent):
  Session A: T09 (interfaces) → push → create PR
  Session B: Reviews T07 PR → approve → merge

Phase 2 (Sequential — B depends on A):
  Session B: pull main (now has T07) → T08 (reporter) → push → create PR
  Session A: Reviews T08 PR → merge
  Session A: T11 (cli) → push → create PR

Phase 2b (Sequential — B depends on A):
  Session B: Reviews T09 PR → approve → merge
  Session B: pull main (now has T09) → T10 (pipeline) → push → create PR

Phase 3 (Sequential — B depends on everything):
  Session A: Reviews T10 PR → merge
  Session B: pull main (has T07+T09+T10) → T12 (integration tests) → push → create PR
  Session A: Reviews T12 → merge
```

### What This Forces

| Pattern | Where It Happens |
|---------|-----------------|
| **Dependency wait** | Session B cannot start T08 until T07 is merged |
| **Cross-session PR review** | Every PR reviewed by the non-author session |
| **Merge order matters** | T12 can only run after T07+T09+T10 are on main |
| **Rebase on updated main** | Session B must `git pull origin main` before each dependent task |
| **Import chain validation** | T08 imports T07; T10 implements T09; T12 tests all together |

---

## 6. PR Review Assignment

| PR | Author | Reviewer | Key Review Points |
|----|--------|----------|-------------------|
| T07 (validator) | A | **B** | Return types, edge cases, Task model import |
| T08 (reporter) | B | **A** | Correctly imports/uses validator from T07 |
| T09 (interfaces) | A | **B** | Protocol definitions complete, typing correct |
| T10 (pipeline) | B | **A** | Correctly implements T09 interfaces |
| T11 (cli) | A | **B** | Argparse correct, module imports work |
| T12 (integration) | B | **A** | All cross-module paths tested |

---

## 7. Success Criteria

| # | Criterion | How to Verify |
|---|-----------|--------------|
| SC-1 | All 6 PRs created, reviewed, and merged | `gh pr list --state merged` shows 6 |
| SC-2 | Every PR has a cross-session review | PR review history shows different author/reviewer |
| SC-3 | `pytest tests/` passes on main after all merges | Exit code 0, 0 failures |
| SC-4 | T08 actually imports from T07 | `grep "from src.validators" src/reports/task_reporter.py` |
| SC-5 | T10 actually implements T09 interfaces | `grep "Processor\|Filter\|Formatter" src/pipeline.py` |
| SC-6 | No merge conflicts occurred | Clean `git log --oneline --graph` |

---

## 8. Session Instructions

### For Session A (paste this when starting the session):

```
You are Session A in a multi-agent PR workflow. 

cd /home/ec2-user/environment/my_projects/git_multi_agent_repo
Read CLAUDE.md first, then read docs/execution_plan/SPRINT_02_CROSS_SESSION_COORDINATION.md

Your tasks (in order):
1. T07: Create src/validators/task_validator.py — validate Task objects
2. T09: Create src/interfaces.py — Protocol classes (Processor, Filter, Formatter)  
3. T11: Create src/cli.py — argparse CLI using validator + string helpers
4. Review Session B's PRs when they appear (T08, T10, T12)

For each task: claim in TASK_CLAIMS.md → branch → code → test → push → create PR.
Wait for Session B to review your PRs before merging.
```

### For Session B (paste this when starting the session):

```
You are Session B in a multi-agent PR workflow.

cd /home/ec2-user/environment/my_projects/git_multi_agent_repo
Read CLAUDE.md first, then read docs/execution_plan/SPRINT_02_CROSS_SESSION_COORDINATION.md

Your tasks (in order):
1. Review Session A's T07 PR → approve and merge
2. T08: Create src/reports/task_reporter.py — uses validator from T07 (must be merged first!)
3. Review Session A's T09 PR → approve and merge
4. T10: Create src/pipeline.py — implements interfaces from T09 (must be merged first!)
5. T12: Create tests/test_integration.py — integration tests (T07+T09+T10 must be merged first!)

For each task: claim in TASK_CLAIMS.md → branch → code → test → push → create PR.
Session A reviews your PRs. You review Session A's PRs.
```

---

**End of Sprint 2 Plan**
