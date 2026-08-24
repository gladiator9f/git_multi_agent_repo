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

## Session Start Checklist (MANDATORY)

Before starting any work:

1. Read this `CLAUDE.md`
2. Read `docs/execution_plan/CURRENT_SPRINT.md` — the active sprint execution plan
3. Sync with remote:
   ```bash
   git fetch origin
   git checkout main
   git pull origin main
   ```
4. Check what other sessions are working on:
   ```bash
   git branch -r
   ```
5. Read `docs/execution_plan/TASK_CLAIMS.md` — see which tasks are claimed
6. **Claim your task**: Update `TASK_CLAIMS.md` on main with your session identifier, commit, and push before branching

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
| PR comments | Notes for the reviewing session |
| Branch names | Scope visibility for other sessions |
| `docs/execution_plan/CURRENT_SPRINT.md` | Task definitions and acceptance criteria |

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
├── CURRENT_SPRINT.md                       — Active sprint (copy of latest)
├── TASK_CLAIMS.md                          — Live task ownership tracker
├── SPRINT_01_SETUP_AND_DEMO.md            — First sprint
└── completed/                              — Archived sprints
```

---

## Operator Tasks (Human — Cannot Be Automated)

| # | Task | When | How |
|---|------|------|-----|
| **O1** | Start Claude Code sessions | Sprint start | Open 2+ terminal tabs, `cd /home/ec2-user/environment/my_projects/git_multi_agent_repo`, run `claude` in each |
| **O2** | Assign agent slots | Sprint start | Tell each session "You are Session A" or "You are Session B" — they'll claim tasks accordingly |
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
3. **GitHub PAT in SSM**: Verify `aws ssm get-parameter --name "/orchestraprime/github/pat" --with-decryption` returns a valid token
4. **Authenticate `gh` CLI** (OPERATOR TASK):
   ```bash
   # Option A: Interactive login
   gh auth login -h github.com

   # Option B: Use PAT from SSM
   export GH_TOKEN=$(aws ssm get-parameter --name "/orchestraprime/github/pat" --with-decryption --query "Parameter.Value" --output text)
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
5. **No dangling branches**: If task is abandoned, delete the branch

---

**End of CLAUDE.md**

*Multiple sessions, isolated branches, coordinated through PRs. File ownership prevents conflicts. The execution plan is the source of truth.*
