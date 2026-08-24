# Operator Quick-Start: Watch Multi-Agent PR Workflow in Action

**Time required**: ~30 minutes for all 3 sprints
**What you'll see**: 2 Claude Code sessions creating branches, writing code, opening PRs, reviewing each other's code, resolving merge conflicts, and merging — all visible in real-time on the GitHub repo.

---

## Pre-Flight (One-Time, ~5 min)

### 1. Update GitHub PAT

Your fine-grained PAT needs push access to `git_multi_agent_repo`.

1. Go to **https://github.com/settings/personal-access-tokens**
2. Edit your token (starts with `github_pat_1...`)
3. **Repository access** → add `git_multi_agent_repo`
4. **Permissions** → **Contents: Read and write**, **Pull requests: Read and write**
5. Click **Regenerate token**
6. If token value changed, update SSM:
   ```bash
   aws ssm put-parameter --name "/orchestraprime/github/pat" --type SecureString --value "NEW_TOKEN_VALUE" --overwrite
   ```

### 2. Push Initial Setup

```bash
cd /home/ec2-user/environment/my_projects/git_multi_agent_repo
./sync_github.sh push "feat: initial multi-agent PR workflow setup"
```

### 3. Authenticate gh CLI

```bash
export GH_TOKEN=$(aws ssm get-parameter --name "/orchestraprime/github/pat" --with-decryption --query "Parameter.Value" --output text)
gh auth status
# Should show: ✓ Logged in to github.com
```

### 4. Push Demo Branches

```bash
git push origin feature/T01-string-helpers
git push origin feature/T02-date-helpers
```

---

## Running the Demo

### Open GitHub in a Browser

Keep **https://github.com/gladiator9f/git_multi_agent_repo** open — you'll see branches, PRs, and merges appear in real-time.

### Sprint 1: Parallel Independent Work (~10 min)

Open **2 terminal tabs** on Cloud9. In each:

```bash
cd /home/ec2-user/environment/my_projects/git_multi_agent_repo
claude
```

**Tab 1 — paste this prompt:**
```
You are Session A in a multi-agent PR workflow demo.

Working directory: /home/ec2-user/environment/my_projects/git_multi_agent_repo

IMPORTANT: Before creating any PR, set the GH_TOKEN env var:
export GH_TOKEN=$(aws ssm get-parameter --name "/orchestraprime/github/pat" --with-decryption --query "Parameter.Value" --output text)

Read CLAUDE.md, then read docs/execution_plan/SPRINT_01_SETUP_AND_DEMO.md.

You own tasks T01, T03, T05. For each task:
1. Claim it in docs/execution_plan/TASK_CLAIMS.md on main (commit + push)
2. Create a feature branch
3. Write the code per the spec in the sprint plan
4. Run tests with python3 -m pytest
5. Push the branch with ./sync_github.sh push "commit message"
6. Create a PR with gh pr create

Start with T01 (string helpers) — the demo branch already has code, so 
check out feature/T01-string-helpers, verify tests pass, then create the PR.
Then do T03 (config settings) from scratch, then T05 (string helper tests 
are already in T01, so bundle T05 with T01 PR).

After creating your PRs, review Session B's PRs (gh pr list, gh pr checkout, gh pr review --approve).
```

**Tab 2 — paste this prompt:**
```
You are Session B in a multi-agent PR workflow demo.

Working directory: /home/ec2-user/environment/my_projects/git_multi_agent_repo

IMPORTANT: Before creating any PR, set the GH_TOKEN env var:
export GH_TOKEN=$(aws ssm get-parameter --name "/orchestraprime/github/pat" --with-decryption --query "Parameter.Value" --output text)

Read CLAUDE.md, then read docs/execution_plan/SPRINT_01_SETUP_AND_DEMO.md.

You own tasks T02, T04, T06. For each task:
1. Claim it in docs/execution_plan/TASK_CLAIMS.md on main (commit + push)
2. Create a feature branch
3. Write the code per the spec in the sprint plan
4. Run tests with python3 -m pytest
5. Push the branch with ./sync_github.sh push "commit message"
6. Create a PR with gh pr create

Start with T02 (date helpers) — the demo branch already has code, so
check out feature/T02-date-helpers, verify tests pass, then create the PR.
Then do T04 (task model) from scratch, then T06 (date helper tests are 
already in T02, so bundle T06 with T02 PR).

After creating your PRs, review Session A's PRs (gh pr list, gh pr checkout, gh pr review --approve).
```

**What to watch on GitHub:**
- Branches appearing (`feature/T01-*`, `feature/T02-*`, etc.)
- PRs being created with proper descriptions
- Cross-session reviews (Session A reviews Session B's PR and vice versa)
- PRs being merged

### Sprint 2: Cross-Session Dependencies (~15 min)

Once Sprint 1 PRs are merged, tell each session to move to Sprint 2.

**Tab 1:**
```
Sprint 1 is done. Move to Sprint 2.
Read docs/execution_plan/SPRINT_02_CROSS_SESSION_COORDINATION.md.
Your tasks: T07 (validator), T09 (interfaces), T11 (CLI).
T07 and T09 have no dependencies — start immediately.
Review Session B's PRs (T08, T10, T12) when they appear.
```

**Tab 2:**
```
Sprint 1 is done. Move to Sprint 2.
Read docs/execution_plan/SPRINT_02_CROSS_SESSION_COORDINATION.md.
Your tasks: T08 (reporter — depends on T07), T10 (pipeline — depends on T09), T12 (integration tests — depends on T07+T09+T10).
First: review and merge Session A's T07 PR. Then start T08.
After T09 is merged, start T10. After T07+T09+T10 are merged, start T12.
```

**What to watch:**
- Session B **waiting** for Session A's T07 PR to merge before starting T08
- Dependency chain: T07 → T08, T09 → T10, T07+T09+T10 → T12
- Import chains working across modules (T08 imports from T07)

### Sprint 3: Merge Conflicts (~10 min)

**Tab 1:**
```
Sprint 2 is done. Move to Sprint 3.
Read docs/execution_plan/SPRINT_03_REFACTOR_AND_RELEASE.md.
Your tasks: T13 (utils exports), T15 (README API ref), T17 (pyproject.toml).
WARNING: T13 and T15 will conflict with Session B's T14 and T16.
Create your PRs quickly — first to merge wins, the other rebases.
```

**Tab 2:**
```
Sprint 2 is done. Move to Sprint 3.
Read docs/execution_plan/SPRINT_03_REFACTOR_AND_RELEASE.md.
Your tasks: T14 (utils imports), T16 (README contributing), T18 (Makefile).
WARNING: T14 and T16 will conflict with Session A's T13 and T15.
If Session A merges first, you must: git fetch origin main && git rebase origin/main, resolve conflicts, then force-push.
```

**What to watch:**
- Both sessions create PRs that touch the same files
- One PR merges first
- The other session rebases and resolves the conflict
- Final state has both changes combined cleanly

---

## What You'll See on GitHub After All 3 Sprints

- **~12 merged PRs** with conventional commit messages
- **Cross-session reviews** on each PR
- **At least 1 rebase/conflict resolution** in Sprint 3
- **Clean main branch** with all modules working together
- **`pytest tests/`** passes with 30+ tests

---

## Monitoring Commands (run from any terminal)

```bash
# Watch branches appear
watch -n 5 'cd /home/ec2-user/environment/my_projects/git_multi_agent_repo && git fetch origin && git branch -r'

# Watch PRs
watch -n 10 'gh pr list --repo gladiator9f/git_multi_agent_repo'

# Check task claims
cat docs/execution_plan/TASK_CLAIMS.md

# Run all tests after merges
cd /home/ec2-user/environment/my_projects/git_multi_agent_repo && git pull origin main && python3 -m pytest tests/ -v
```
