# Multi-Agent Git PR Workflow — Setup Documentation

**Created**: 2026-08-24
**Status**: Setup Complete — Ready for First Sprint

---

## What Was Created

### Core Workflow Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Instructions for any Claude Code session opening this repo — session start/end checklists, branch conventions, conflict avoidance, operator tasks |
| `sync_github.sh` | Push to GitHub with PAT from AWS SSM (matches existing OrchestraPrime sync pattern) |
| `README.md` | Quick-start guide |
| `.gitignore` | Python standard ignores |
| `requirements.txt` | pytest dependency |

### Execution Plan Framework

| File | Purpose |
|------|---------|
| `docs/execution_plan/MULTI_AGENT_PR_EXECUTION_TEMPLATE.md` | Reusable sprint template (adapted from Doscierge Agent Teams v1.4.0) — agent slots, task breakdown, file ownership matrix, PR review assignments, conflict resolution |
| `docs/execution_plan/SPRINT_01_SETUP_AND_DEMO.md` | Demo sprint with 6 tasks split across 2 sessions |
| `docs/execution_plan/CURRENT_SPRINT.md` | Copy of active sprint (currently Sprint 1) |
| `docs/execution_plan/TASK_CLAIMS.md` | Live tracker — sessions claim tasks here before branching |
| `docs/execution_plan/completed/` | Archive directory for finished sprints |

### Project Scaffolding

```
src/
├── __init__.py
├── utils/
│   └── __init__.py          (T01/T02 will add string_helpers.py, date_helpers.py)
├── config/
│   └── __init__.py          (T03 will add settings.py)
└── models/
    └── __init__.py          (T04 will add task.py)
tests/
└── __init__.py              (T05/T06 will add test files)
```

### Demo Branches (Pre-Staged)

| Branch | Task | Contents | PR Status |
|--------|------|----------|-----------|
| `feature/T01-string-helpers` | T01 | `src/utils/string_helpers.py` + `tests/test_string_helpers.py` | Ready to push & create PR |
| `feature/T02-date-helpers` | T02 | `src/utils/date_helpers.py` + `tests/test_date_helpers.py` | Ready to push & create PR |

---

## How to Start Using It

### One-Time Setup (Operator — ~5 minutes)

1. **Authenticate `gh` CLI** (required for PR creation):
   ```bash
   cd /home/ec2-user/environment/my_projects/git_multi_agent_repo
   export GH_TOKEN=$(aws ssm get-parameter --name "/orchestraprime/github/pat" --with-decryption --query "Parameter.Value" --output text)
   gh auth status
   ```

2. **Push initial setup to GitHub**:
   ```bash
   ./sync_github.sh push "feat: initial multi-agent PR workflow setup"
   ```

3. **Push demo branches**:
   ```bash
   git push origin feature/T01-string-helpers
   git push origin feature/T02-date-helpers
   ```

4. **Create demo PRs** (optional — or let sessions do it):
   ```bash
   git checkout feature/T01-string-helpers
   gh pr create --title "feat(utils): add string helper functions" --body "Task T01 from Sprint 1"
   git checkout feature/T02-date-helpers
   gh pr create --title "feat(utils): add date helper functions" --body "Task T02 from Sprint 1"
   git checkout main
   ```

### Running a Sprint (Operator — ~2 minutes per sprint)

1. Open 2 terminal tabs, `cd` to the repo in each
2. Run `claude` in each tab
3. Tell Session A: _"You are Session A. Read CLAUDE.md, then claim and execute your Sprint 1 tasks (T01, T03, T05)."_
4. Tell Session B: _"You are Session B. Read CLAUDE.md, then claim and execute your Sprint 1 tasks (T02, T04, T06)."_
5. Watch them work in parallel — creating branches, writing code, pushing, creating PRs
6. Optionally tell one session to review the other's PR

### Running from Your Other Claude Code Session

If you already have a second Claude Code session running:
1. In that session, navigate to this repo: `cd /home/ec2-user/environment/my_projects/git_multi_agent_repo`
2. Tell it: _"You are Session B. Read CLAUDE.md and the Sprint 1 execution plan, then claim and execute tasks T02, T04, T06."_

---

## How to Apply to Other Repos

### Step-by-step for an existing repo

1. **Copy the workflow files**:
   ```bash
   TARGET_REPO="/home/ec2-user/environment/my_projects/<your-repo>"
   
   # Copy CLAUDE.md (edit project-specific sections)
   cp CLAUDE.md "$TARGET_REPO/"
   
   # Copy execution plan template
   mkdir -p "$TARGET_REPO/docs/execution_plan"
   cp docs/execution_plan/MULTI_AGENT_PR_EXECUTION_TEMPLATE.md "$TARGET_REPO/docs/execution_plan/"
   
   # Copy sync script (edit GITHUB_REPO and LOCAL_DIR)
   cp sync_github.sh "$TARGET_REPO/"
   chmod +x "$TARGET_REPO/sync_github.sh"
   ```

2. **Edit CLAUDE.md** in the target repo:
   - Update project name, repo URL, description
   - Adjust branch naming to match your conventions
   - Keep the workflow rules, checklists, and operator tasks as-is

3. **Edit sync_github.sh**:
   - Change `GITHUB_REPO` to your repo's `owner/repo`
   - Change `LOCAL_DIR` to the target repo path

4. **Create your first sprint** from the template:
   - Copy `MULTI_AGENT_PR_EXECUTION_TEMPLATE.md` to `SPRINT_01_<name>.md`
   - Fill in tasks, file ownership, agent slot assignments
   - Copy to `CURRENT_SPRINT.md`
   - Create `TASK_CLAIMS.md`

5. **Start sessions** and follow the workflow

### Repos ready to adopt

| Repo | Path | GitHub Remote |
|------|------|--------------|
| aws_partner_analysis | `/home/ec2-user/environment/my_projects/aws_partner_analysis/` | gladiator9f/aws_partner_analysis |
| orchestraprime-saas-monetization | `/home/ec2-user/environment/my_projects/orchestraprime-saas-monetization/` | (check remote) |
| fda_inspection_assistant | `/home/ec2-user/environment/my_projects/fda_inspection_assistant/` | (check remote) |

---

## Architecture: How Multi-Agent PR Workflow Operates

```
┌─────────────────────────────────────────────────────────┐
│                    AWS Cloud9 Machine                     │
│                                                           │
│  ┌──────────────┐         ┌──────────────┐               │
│  │ Claude Code   │         │ Claude Code   │              │
│  │ Session A     │         │ Session B     │              │
│  │               │         │               │              │
│  │ 1. Read       │         │ 1. Read       │              │
│  │    CLAUDE.md  │         │    CLAUDE.md  │              │
│  │ 2. Claim T01  │         │ 2. Claim T02  │              │
│  │ 3. Branch     │         │ 3. Branch     │              │
│  │ 4. Code       │         │ 4. Code       │              │
│  │ 5. Push       │         │ 5. Push       │              │
│  │ 6. Create PR  │         │ 6. Create PR  │              │
│  │ 7. Review B's │         │ 7. Review A's │              │
│  │    PR         │         │    PR         │              │
│  └──────┬───────┘         └──────┬───────┘               │
│         │                        │                        │
│         └────────┬───────────────┘                        │
│                  │                                        │
│         ┌────────▼────────┐                               │
│         │   Local Git Repo │                              │
│         │   (shared .git)  │                              │
│         └────────┬────────┘                               │
│                  │                                        │
└──────────────────┼────────────────────────────────────────┘
                   │ push/pull
         ┌─────────▼─────────┐
         │   GitHub Remote    │
         │   (PRs, Reviews)   │
         └───────────────────┘
```

### Coordination Mechanisms

| Mechanism | What It Coordinates |
|-----------|-------------------|
| **TASK_CLAIMS.md** (on main) | Who's working on what — prevents duplicate work |
| **Branch names** | Scope visibility — other sessions see `feature/T01-*` in `git branch -r` |
| **File ownership** (in execution plan) | Prevents conflicts — each file owned by exactly one task |
| **PR reviews** | Quality gate — cross-session review before merge |
| **Rebase-before-push** | Merge hygiene — always rebase on latest main |

### Comparison to Doscierge Agent Teams Model

| Aspect | Doscierge Agent Teams | Multi-Agent PR |
|--------|----------------------|----------------|
| **Isolation** | File ownership within same branch | Separate branches per task |
| **Coordination** | KANBAN + TRACEABILITY_MATRIX | TASK_CLAIMS.md + PR comments |
| **Review** | Lead DoD gate | Cross-session PR review |
| **Merge** | Direct commit to main | PR merge (squash preferred) |
| **Compliance** | GAMP 5, ALCOA+, adversarial DoD | Lightweight — conventional commits, test pass |
| **Complexity** | 17 mandatory sections, 12 closing tasks | 10 sections, 5 closing tasks |

---

## Manual Steps Still Needed

| # | Step | Blocker | Resolution |
|---|------|---------|-----------|
| 1 | `gh auth login` | gh CLI token expired | Run `export GH_TOKEN=$(aws ssm get-parameter ...)` or `gh auth login` interactively |
| 2 | Initial push to GitHub | Not yet pushed | Run `./sync_github.sh push "initial setup"` |
| 3 | Demo branch push | Not yet pushed | Run `git push origin feature/T01-string-helpers feature/T02-date-helpers` |

---

**End of Setup Documentation**
