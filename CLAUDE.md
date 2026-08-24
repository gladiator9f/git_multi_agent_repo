# CLAUDE.md — Multi-Agent Git PR Workflow

**Project**: git_multi_agent_repo — Multi-Session Claude Code PR Workflow
**Purpose**: Coordinate multiple Claude Code sessions working on the same codebase via Git branches and Pull Requests
**Repo**: https://github.com/gladiator9f/git_multi_agent_repo.git
**Created**: 2026-08-24

---

## How This Works

Multiple Claude Code sessions run simultaneously on the same Cloud9 machine. Each session:
1. Claims a task from the execution plan
2. Creates a feature branch (`feature/<task-id>-<short-desc>`)
3. Does the work in isolation on that branch
4. Pushes and creates a PR via `gh pr create` or `./sync_github.sh push`
5. Another session reviews the PR

**Key principle**: Sessions coordinate through Git — branches, PRs, and the task claims file. No shared state outside of Git.

---

## CRITICAL: Git Worktrees Required for Parallel Sessions

**Two sessions sharing the same working directory WILL cause branch collisions.** When Session A checks out a feature branch, Session B's `git checkout` switches the entire directory to a different branch — destroying Session A's working state.

**Solution**: Each session MUST work in its own **git worktree**.

### Setup (one-time per session)

```bash
# From the main repo directory
REPO_DIR=/home/ec2-user/environment/my_projects/git_multi_agent_repo
WORKTREE_BASE=/home/ec2-user/environment/my_projects/git_multi_agent_repo_worktrees

# Create a worktree for each session
git worktree add "$WORKTREE_BASE/session-a" -b session-a-workspace main
git worktree add "$WORKTREE_BASE/session-b" -b session-b-workspace main
```

### How it works

- Each worktree is an isolated directory with its own checked-out branch
- All worktrees share the same `.git` database (commits, remotes, history)
- Session A works in `$WORKTREE_BASE/session-a`, Session B in `$WORKTREE_BASE/session-b`
- The main repo directory stays on `main` and is used for coordination tasks only (updating TASK_CLAIMS.md, etc.)

### Per-task workflow in a worktree

```bash
cd $WORKTREE_BASE/session-a
git fetch origin
git checkout -b feature/T07-task-validator origin/main
# ... do work, commit, push ...
# When done, switch back:
git checkout main
```

### Cleanup after sprint

```bash
# Remove worktrees when no longer needed
git worktree remove "$WORKTREE_BASE/session-a"
git worktree remove "$WORKTREE_BASE/session-b"
# List remaining worktrees
git worktree list
```

> **Lesson learned (Sprint 1)**: Without worktrees, Session A and Session B repeatedly overwrote each other's branches, causing commits to land on wrong branches and requiring multiple force-resets. Worktrees eliminated this entirely.

---

## Session Start Checklist (MANDATORY)

Before starting any work:

1. Read this `CLAUDE.md`
2. **Find your sprint assignment**:
   - Read `docs/execution_plan/SESSION_REGISTRY.md` — find your session's assigned sprint
   - Read that sprint's execution plan (e.g., `SPRINT_02_CROSS_SESSION_COORDINATION.md`)
   - If your operator prompt specifies a sprint, use that; otherwise fall back to `CURRENT_SPRINT.md`
3. **Check for cross-sprint file collisions**:
   - Read `docs/execution_plan/FILE_OWNERSHIP_MATRIX.md`
   - If any file you plan to touch is also claimed by a task in another active sprint, follow the Cross-Sprint Conflict Protocol in that file
4. Sync with remote:
   ```bash
   git fetch origin
   git checkout main
   git pull origin main
   ```
5. Check what other sessions are working on:
   ```bash
   git branch -r
   ```
6. Read `docs/execution_plan/TASK_CLAIMS.md` — see which tasks are claimed
7. **Claim your task**: Update `TASK_CLAIMS.md` on main with your session identifier, commit, and push before branching
8. **Update registry**: Update your row in `SESSION_REGISTRY.md` with status `🟡 Active`

---

## Branch Naming Convention

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/<task-id>-<short-desc>` | `feature/T01-add-string-helpers` |
| Bugfix | `bugfix/<task-id>-<short-desc>` | `bugfix/T05-fix-login-redirect` |
| Hotfix | `hotfix/<desc>` | `hotfix/critical-security-patch` |

---

## Git Workflow Rules

### Creating a Branch

```bash
git checkout main
git pull origin main
git checkout -b feature/T01-add-string-helpers
```

### Committing (Conventional Commits — MANDATORY)

```
feat(utils): add string helper functions
fix(api): correct timeout handling in health check
docs(readme): update setup instructions
test(utils): add unit tests for string helpers
refactor(db): extract connection pooling logic
```

### Pushing & Creating a PR

```bash
# Push branch
./sync_github.sh push "feat(utils): add string helper functions"

# Create PR (if gh CLI is authenticated)
gh pr create --title "feat(utils): add string helpers" --body "$(cat <<'EOF'
## Summary
- Added slugify, truncate, sanitize_html utility functions
- Full test coverage

## Test Plan
- [ ] pytest tests/test_string_helpers.py passes
- [ ] No import errors

## Task Reference
Task T01 from Sprint 1 Execution Plan

🤖 Generated with Claude Code
EOF
)"
```

### Reviewing a PR (from another session)

```bash
# List open PRs
gh pr list

# Check out the PR
gh pr checkout <pr-number>

# Run tests
pytest tests/

# Approve or request changes
gh pr review <pr-number> --approve --body "LGTM - tests pass, code clean"
gh pr review <pr-number> --request-changes --body "See inline comments"
```

### Merging

```bash
gh pr merge <pr-number> --squash --delete-branch
```

---

## Conflict Avoidance Rules

1. **File Ownership**: Each task in the execution plan specifies which files/directories it touches. Sessions MUST NOT modify files outside their task scope.
2. **Check Before Starting**: Run `git branch -r` and review `TASK_CLAIMS.md` before starting work.
3. **Small, Focused PRs**: One PR per task. Don't bundle unrelated changes.
4. **Rebase Before PR**: Always rebase on latest main before pushing:
   ```bash
   git fetch origin main
   git rebase origin/main
   ```

---

## Parallel Session Coordination

### How sessions avoid conflicts

- The execution plan assigns tasks to **agent slots** (Session A, Session B, etc.)
- Each session updates `TASK_CLAIMS.md` on main when it starts a task
- File ownership is explicit per task — no two tasks touch the same files
- If a conflict is unavoidable, one session creates the PR first, the other rebases after merge

### Communication between sessions

| Channel | Purpose |
|---------|---------|
| `TASK_CLAIMS.md` on main | Who's working on what |
| `SESSION_REGISTRY.md` on main | Which session is on which sprint |
| `FILE_OWNERSHIP_MATRIX.md` | Global cross-sprint file collision map |
| PR comments | Notes for the reviewing session |
| Branch names | Scope visibility for other sessions |

### Cross-Sprint Parallel Work

Sessions can work on **different sprints simultaneously** (e.g., Session A on Sprint 2 while Session B on Sprint 3). This works because:

- **Worktrees** isolate each session's branch regardless of sprint
- **TASK_CLAIMS.md** spans all sprints in one file
- **FILE_OWNERSHIP_MATRIX.md** provides a global view of which files are contested across all active sprints
- **SESSION_REGISTRY.md** maps each session to its sprint so sessions know what each other is working on

**Rules for cross-sprint work:**
1. **Read-only imports are safe** — importing from a merged file owned by a completed sprint is fine
2. **Write collisions require sequencing** — if your task modifies a file another sprint also modifies, first PR merged wins; second session rebases
3. **Interface changes break downstream** — do not change the public API of merged code without updating all importers (check the dependency graph in `FILE_OWNERSHIP_MATRIX.md`)
4. **Cross-sprint dependencies must be satisfied** — check the dependency flags in `FILE_OWNERSHIP_MATRIX.md` before starting

---

## Sync Script Usage

For branch work (most common):
```bash
# Push current branch
./sync_github.sh push "feat(utils): add string helpers"
```

The script handles PAT retrieval from AWS SSM, remote auth, and push. For direct git commands, configure credentials first (see Operator Tasks).

---

## Execution Plan Structure

```
docs/execution_plan/
├── MULTI_AGENT_PR_EXECUTION_TEMPLATE.md   — Reusable sprint template
├── SESSION_REGISTRY.md                     — Session → sprint mapping (supports cross-sprint parallelism)
├── FILE_OWNERSHIP_MATRIX.md               — Global cross-sprint file collision map
├── CURRENT_SPRINT.md                       — Default sprint (fallback when no registry entry)
├── TASK_CLAIMS.md                          — Live task ownership tracker (all sprints)
├── SPRINT_01_SETUP_AND_DEMO.md            — First sprint
├── SPRINT_02_CROSS_SESSION_COORDINATION.md — Second sprint
├── SPRINT_03_REFACTOR_AND_RELEASE.md      — Third sprint
└── completed/                              — Archived sprints
```

---

## Operator Tasks (Human — Cannot Be Automated)

| # | Task | When | How |
|---|------|------|-----|
| **O1** | Start Claude Code sessions | Sprint start | Open 2+ terminal tabs, `cd /home/ec2-user/environment/my_projects/git_multi_agent_repo`, run `claude` in each |
| **O2** | Assign agent slots + sprint | Sprint start | Tell each session its ID AND sprint: "You are Session A on Sprint 2" — sessions can be on different sprints |
| **O3** | Authenticate `gh` CLI (one-time) | Pre-setup | `gh auth login` with PAT from SSM, or set `GH_TOKEN` env var |
| **O4** | Review/merge PRs (optional) | During sprint | Sessions can review each other's PRs, or operator does it via GitHub web UI |
| **O5** | Resolve conflicts (if any) | As needed | If two PRs touch overlapping files, decide merge order |
| **O6** | Sprint retrospective | Sprint end | Review what worked, adjust execution plan template |
| **O7** | Apply to other repos | After validation | Copy CLAUDE.md + template to other project repos, adapt project-specific sections |

---

## Pre-Setup Checklist (One-Time — Operator)

Before the first sprint:

1. **Git initialized** ✅ (done by setup script)
2. **Remote configured** ✅ (done by setup script)
3. **GitHub PAT in SSM**: Verify `aws ssm get-parameter --name "/orchestraprime/github/pat_multi_agent_repo" --with-decryption` returns a valid token
4. **Authenticate `gh` CLI** (OPERATOR TASK):
   ```bash
   # Option A: Interactive login
   gh auth login -h github.com

   # Option B: Use PAT from SSM
   export GH_TOKEN=$(aws ssm get-parameter --name "/orchestraprime/github/pat_multi_agent_repo" --with-decryption --query "Parameter.Value" --output text)
   gh auth status
   ```
5. **Initial push**: Run `./sync_github.sh push "initial setup"` to push scaffolding to GitHub
6. **Verify**: Visit https://github.com/gladiator9f/git_multi_agent_repo to confirm

---

## Applying to Other Repos

Once this workflow is validated here:

1. Copy `CLAUDE.md` to the target repo — adapt the project-specific sections (repo URL, project name)
2. Copy `docs/execution_plan/MULTI_AGENT_PR_EXECUTION_TEMPLATE.md`
3. Copy `sync_github.sh` — update `GITHUB_REPO` and `LOCAL_DIR` variables
4. Create the first sprint execution plan from the template
5. Start multiple Claude Code sessions in that repo
6. Each session reads CLAUDE.md and follows the workflow

### Repos ready to adopt this pattern:
```
/home/ec2-user/environment/my_projects/aws_partner_analysis/
/home/ec2-user/environment/my_projects/orchestraprime-saas-monetization/
/home/ec2-user/environment/my_projects/fda_inspection_assistant/
```

---

## Session End Checklist

1. **Commit**: All work committed on your feature branch
2. **Push**: Branch pushed to origin
3. **PR**: PR created (if task is complete)
4. **Claims**: `TASK_CLAIMS.md` updated with your status
5. **Registry**: `SESSION_REGISTRY.md` updated (status → `✅ Complete` if all tasks done)
6. **No dangling branches**: If task is abandoned, delete the branch

---

**End of CLAUDE.md**

*Multiple sessions, isolated branches, coordinated through PRs. File ownership prevents conflicts. The execution plan is the source of truth.*
