# CLAUDE.md — Multi-Agent Git PR Workflow

**Repo**: https://github.com/gladiator9f/git_multi_agent_repo.git

---

## Tier 1 — Core Protocol (Always Active)

These rules apply to every session, every repo. No pre-planning required.

### 1.1 Worktrees — Non-Negotiable

Two sessions sharing one working directory **will** cause branch collisions. Each session MUST work in its own git worktree.

```bash
WORKTREE_BASE="$(git rev-parse --show-toplevel)_worktrees"
git worktree add "$WORKTREE_BASE/session-a" main
git worktree add "$WORKTREE_BASE/session-b" main
```

- Each worktree is an isolated directory with its own checked-out branch
- All worktrees share the same `.git` database (commits, remotes, history)
- The main repo directory stays on `main` for coordination only

### 1.2 Session Start

1. Read this `CLAUDE.md`
2. Sync: `git fetch origin && git pull origin main`
3. Check what's in flight: `git branch -r` and read `ACTIVE_WORK.md`
4. **Declare your work** in `ACTIVE_WORK.md` before branching (see 1.5)

### 1.3 Branches and Commits

**Branch naming:**
```
feature/<short-desc>        — new functionality
bugfix/<short-desc>         — fixing a defect
refactor/<short-desc>       — restructuring without behavior change
hotfix/<short-desc>         — urgent production fix
```

**Conventional commits (mandatory):**
```
feat(scope): what changed
fix(scope): what was broken
docs(scope): documentation only
test(scope): adding or fixing tests
refactor(scope): no behavior change
```

### 1.4 PR Workflow

```bash
# Create branch from latest main
git checkout -b feature/add-auth-middleware origin/main

# Work, commit, then rebase before pushing
git fetch origin main
git rebase origin/main

# Push and create PR
./sync_github.sh push "feat(auth): add middleware"
export GH_TOKEN=$(aws ssm get-parameter --name "/orchestraprime/github/pat_multi_agent_repo" \
  --with-decryption --query "Parameter.Value" --output text)
gh pr create --title "feat(auth): add middleware" --body "..."

# Another session reviews
gh pr list
gh pr checkout <pr-number>
pytest tests/
gh pr comment <pr-number> --body "LGTM — tests pass"
gh pr merge <pr-number> --squash --delete-branch
```

### 1.5 ACTIVE_WORK.md — Live Declaration

Instead of pre-mapped file ownership, each session **declares what it's working on as it goes**. This is the only coordination file that matters at runtime.

```markdown
# Active Work

| Session | Branch | What I'm Doing | Key Files I'm Touching | Status |
|---------|--------|---------------|----------------------|--------|
| A | feature/add-auth | Auth middleware | src/auth/, tests/test_auth.py | 🟡 In Progress |
| B | bugfix/fix-date-parse | Date parsing edge case | src/utils/date_helpers.py | 🟡 In Progress |
```

**Rules:**
- Update this file on `main` **before** creating your feature branch
- List the files/directories you expect to touch — best guess is fine, update if scope changes
- If you see another session touching the same files, **comment on their PR or wait for it to merge** before starting yours
- Remove your row when your PR is merged

**How to update:**
```bash
# From the main repo directory (not your worktree)
git checkout main && git pull origin main
# Edit ACTIVE_WORK.md
git add ACTIVE_WORK.md
git commit -m "claim: <what you're doing> — Session <X>"
git push origin main
```

### 1.6 Conflict Resolution

Conflicts are normal. The protocol:

1. **First PR merged wins** — no negotiation needed
2. **Second session rebases**: `git fetch origin main && git rebase origin/main`
3. **Resolve conflicts**, keeping both sessions' changes
4. **Force-push the rebased branch**: `git push --force-with-lease`
5. If the conflict is complex, comment on the PR describing what changed

### 1.7 Session End

1. All work committed and pushed on your feature branch
2. PR created if task is complete
3. `ACTIVE_WORK.md` updated (row removed or status → `✅ Merged`)
4. No dangling branches

---

## Tier 2 — Execution Plan Mode (Optional)

Use this when you want pre-scripted coordination: known tasks, assigned sessions, explicit dependencies. Good for structured sprints, demos, onboarding exercises.

**Skip this tier entirely for ad-hoc real-world development** — Tier 1 is sufficient.

### 2.1 When to Use Tier 2

- You know the tasks and their scope upfront
- You want to demo or train on the multi-agent workflow
- You need to enforce dependency ordering (Task B waits for Task A to merge)
- You're coordinating 3+ sessions and want a pre-agreed division of labor

### 2.2 Execution Plan Structure

```
docs/execution_plan/
├── TEMPLATE.md                    — Reusable sprint template
├── SPRINT_<NN>_<NAME>.md         — Sprint plans (when using Tier 2)
└── completed/                     — Archived sprints
```

### 2.3 Sprint Plan Contents

A sprint execution plan defines:

| Section | Purpose |
|---------|---------|
| Agent Slots | Which session handles which tasks |
| Task Breakdown | Tasks with owners, files, dependencies, branches |
| File Ownership | Explicit per-task — no overlap unless deliberate |
| Execution Timeline | Phased ordering showing dependency chains |
| PR Review Assignment | Cross-session review pairings |
| Success Criteria | How to verify the sprint is complete |
| Session Prompts | Copy-paste prompts for the operator to give each session |

### 2.4 Task Dependencies

In Tier 2, dependencies are explicit:

```
T07 (validator)  →  T08 (reporter imports validator)  →  T12 (integration tests)
T09 (interfaces) →  T10 (pipeline implements interfaces) →  T12
```

A session **must not start** a dependent task until the upstream PR is merged to main.

### 2.5 Deliberate Merge Conflicts

Tier 2 can deliberately assign overlapping files to test conflict resolution:
- Both sessions modify `src/utils/__init__.py` — first merged wins, other rebases
- Useful for training, but avoid in real production sprints

---

## Sync Script

```bash
./sync_github.sh push "commit message"
```

Handles PAT retrieval from AWS SSM (`/orchestraprime/github/pat_multi_agent_repo`), remote auth, and push.

---

## Operator Tasks

| # | Task | When |
|---|------|------|
| **O1** | Start Claude Code sessions in separate terminals | Before work begins |
| **O2** | Tell each session its ID: "You are Session A" | Session start |
| **O3** | Set `GH_TOKEN` env var or run `gh auth login` (one-time) | Pre-setup |
| **O4** | Merge PRs or let sessions merge after review | During work |
| **O5** | Decide merge order if two PRs touch same files | As needed |

For Tier 2 add: assign sprint ("You are Session A — start Sprint 2 tasks T07, T09, T11").

---

## Applying to Other Repos

1. Copy this `CLAUDE.md` — update repo URL and SSM parameter name
2. Copy `sync_github.sh` — update `GITHUB_REPO` and `LOCAL_DIR`
3. Create `ACTIVE_WORK.md` (empty table)
4. Optionally copy `docs/execution_plan/TEMPLATE.md` if using Tier 2

---

## Reference: Existing Sprint Plans (Tier 2 Demo)

These are the training sprints used to validate this workflow:

| Sprint | File | What It Demonstrates |
|--------|------|---------------------|
| Sprint 1 | `SPRINT_01_SETUP_AND_DEMO.md` | Parallel independent work, no conflicts |
| Sprint 2 | `SPRINT_02_CROSS_SESSION_COORDINATION.md` | Dependency chains, cross-session PR review |
| Sprint 3 | `SPRINT_03_REFACTOR_AND_RELEASE.md` | Deliberate merge conflicts, shared file resolution |

Sprint 1 is complete (PRs #1-#4 merged). Sprints 2-3 are available for continued training.
