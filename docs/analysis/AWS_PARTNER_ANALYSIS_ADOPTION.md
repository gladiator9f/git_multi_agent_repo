# AWS Partner Analysis — Multi-Agent Git PR Workflow Adoption Analysis

**Target repo**: `/home/ec2-user/environment/my_projects/aws_partner_analysis`
**Reference workflow**: `/home/ec2-user/environment/my_projects/git_multi_agent_repo` (CLAUDE.md Tier 1/Tier 2 protocol)
**Analysis date**: 2026-08-24
**Pilot sub-project**: PetID (`docs/pets_face_recon/`)

---

## Executive Summary

`aws_partner_analysis` is a single **monorepo** (one `.git`, no nested repos) holding ~60 sub-projects under `docs/`, pushed to `github.com/gladiator9f/aws_partner_analysis` on branch **`master`** (not `main`). The working tree is clean, there is one worktree (the main checkout), and 10,700 tracked files totaling only **~240MB** — the 4GB on-disk bulk is git-ignored media, so additional worktrees are cheap.

The current commit workflow is the **opposite** of the target PR workflow: `sync_github.sh` does `git add -A` across the entire monorepo, commits with a timestamp message, and pushes `master` with `--force-with-lease` falling back to **`--force`**. There are no branches, no PRs, no conventional-commit discipline (a mix of descriptive and "Sync ... UTC" messages).

Adoption is feasible with modest pre-configuration:

1. **Fix the sync script** (branch-aware, scoped `git add`, remove the `--force` fallback) — this is the single highest-risk item.
2. **Reconcile `master` vs `main`** — recommend keeping `master` and adapting the protocol text (zero-risk), with an optional later rename.
3. **Add one `ACTIVE_WORK.md` at repo root** with a Sub-Project column.
4. **Pilot on PetID** — dormant since 2026-06-09, self-contained (224 tracked files, all under one path), has its own CLAUDE.md and a real test suite (14 test files, 169 tests passing at Sprint 7) to verify PRs against.
5. **Stay away from `docs/doscierge/` and `docs/agent/` initially** — they account for ~595 of the file-touches in the last 14 days and are under active development.

Two credential notes: the origin remote URL currently has the **PAT embedded in cleartext** in `.git/config` (rewritten on every sync run), and worktrees share that remote config — convenient for the pilot, but worth moving to a credential helper eventually. `gh` CLI v2.82.0 is installed; verify the fine-grained PAT has **Pull requests: Read and write** before the first `gh pr create`.

---

## Repo Overview

### Git state (verified 2026-08-24)

| Item | Value |
|------|-------|
| Repo type | **Monorepo** — single `.git` at root; `find` confirms **no nested `.git`** anywhere |
| Branch | `master` (only branch, local and remote) — **workflow docs assume `main`** |
| Remote | `origin → github.com/gladiator9f/aws_partner_analysis.git` — **PAT embedded in the URL** in `.git/config` |
| Working tree | Clean; no stash; single worktree (`git worktree list` shows only the main checkout at `7696ba7d`) |
| Tracked files | 10,700 files, **0.24 GB** checkout size |
| `.git` size | 625 MB on disk (pack: 478.55 MiB, 3,686 loose objects) |
| On-disk size | ~4 GB total (`docs/` = 3.1 GB) — the delta vs 0.24 GB tracked is **ignored** media (mp4/mp3/pdf/pptx, node_modules, large JSONs) |
| Largest tracked file | 22.5 MB (`docs/agent/longtail/.../email1of2.zip`) — all files well under GitHub's 100 MB limit |
| Git identity | `AWS Partner Bot <aws-partner-bot@orchestraprime.ai>` (set by sync script on every run) |
| gh CLI | v2.82.0 installed at `/usr/bin/gh` |
| Cron | No crontab — sync commits are manual, not scheduled (good: no automation will race the PR flow) |
| Disk | 14 GB free on the 45 GB root volume — several worktrees fit comfortably |

### Current commit workflow (`sync_github.sh`, repo root)

```
PAT from SSM /orchestraprime/github/pat
→ git config bot identity → remote set-url with embedded PAT
→ git add -A (ENTIRE monorepo)
→ commit (custom msg or "Sync AWS Partner Analysis updates - <timestamp>")
→ git push origin <current-branch> --force-with-lease
→ ON FAILURE: git push --force        ← incompatible with multi-session work
```

Three properties break the multi-agent PR model:

- **`git add -A` from repo root** sweeps every sub-project's uncommitted changes into one commit — a feature-branch commit would carry unrelated work.
- **`--force` fallback** can silently erase another session's pushed commits.
- Assumes it always runs from the main checkout (`LOCAL_DIR` hardcoded), so it can't push a feature branch from inside a worktree.

The reference repo's `sync_github.sh` (`git_multi_agent_repo/sync_github.sh`) is branch-aware but retains `add -A` and the `--force` fallback, and hardcodes its own `LOCAL_DIR` — copy it as a starting point, but apply the fixes in the Pre-Configuration Checklist.

### Commit-message state

`git log` shows a mix: descriptive one-liners ("Sprint 8: Fix PSG count..."), timestamp syncs ("Sync AWS Partner Analysis updates - 2026-08-23..."), and long multi-clause messages. **No conventional-commit prefixes anywhere.** Adopting `feat(scope):` etc. is a net-new discipline, not a migration.

### Existing CLAUDE.md files (16)

| Path | Scope |
|------|-------|
| `CLAUDE.md` (root) | OrchestraPrime Growth Initiatives — marketing/GTM context, session checklists; last updated 2026-02-05; **no git-workflow section** |
| `docs/pets_face_recon/CLAUDE.md` | PetID — full project instructions incl. agent-teams model with **pre-scripted file ownership** (see PetID Deep Dive) |
| `docs/doscierge/CLAUDE.md` | Doscierge (ACTIVE) |
| `docs/doscierge/docs/agents_team_execution_plan/anda_site/CLAUDE.md` | ANDA site sub-scope (ACTIVE) |
| `docs/slm_dm_regulatory_anda/CLAUDE.md` | SLM regulatory |
| `docs/prince_innov_hub/Biomedical_AI_Agent/CLAUDE.md` | Princeton CAP |
| `docs/agent/CLAUDE.md` | Agent/FDE work (ACTIVE) |
| `docs/nj-connect/tie-collab/fde/CLAUDE.md` | FDE collab |
| `docs/bio-nj/planning/partnering/traceability/CLAUDE.md` | BioNJ |
| `docs/biomap/networking_presentation/CLAUDE.md` | BioMap |
| `docs/aws/innovate_idea/{gumroad_products,consulting_fractional,nj_ron_notary}/CLAUDE.md` | Idea explorations (3 files) |
| `freelance-projects/{ofac-screening-chrome-extension,aws-cdk-sanctions-screening,claude_mcp_orchprime}/CLAUDE.md` | Freelance (3 files, dormant since ~Feb) |

None of them mention branches, PRs, worktrees, or conventional commits — no direct conflicts to remove, only additions to make. The one **semantic** conflict is PetID's pre-scripted file-ownership table (addressed below).

---

## Sub-Project Inventory

Activity = files touched in commits since 2026-08-10 (`git log --since=2026-08-10 --name-only`).

| Sub-project | Path | Size (disk) | Tracked activity (14d) | Risk to pilot on | Notes |
|-------------|------|-------------|------------------------|------------------|-------|
| **PetID** | `docs/pets_face_recon/` | 19 MB / 225 files | **0 — dormant since 2026-06-09** | **LOW — chosen pilot** | Own CLAUDE.md, real tests, deployed (petid.orchestraprime.ai) but not under change |
| Doscierge | `docs/doscierge/` | 1.5 GB | **297 files — very active** | **HIGH** | ANDA compliance product; Sprint 8 in flight; adopt LAST |
| Agent / Longtail | `docs/agent/` | 129 MB | **298 files — very active** | **HIGH** | Kenzai/Longtail FDE prep; adopt LAST |
| Claude opportunities | `docs/claude/` | 142 MB | 36 files | MEDIUM | Ongoing |
| Other opp (lifestyle) | `docs/other_opp/` | — | 16 files | MEDIUM | B&B/deli analysis, recent |
| YT scrap | `docs/yt_scrap/` | — | 15 files | MEDIUM | Recent |
| BioMap | `docs/biomap/` | 3.5 MB | 13 files | MEDIUM | Recent |
| NJ Connect | `docs/nj-connect/` | 61 MB | 6 files | LOW-MED | Tue/Thu/Sat review cadence |
| Reshoring Pharma NJ | `docs/reshoring_pharma_nj/` | 923 MB | 0 | LOW | Dormant |
| SLM Regulatory ANDA | `docs/slm_dm_regulatory_anda/` | 236 MB | 0 | LOW | Dormant; own CLAUDE.md |
| BioNJ | `docs/bio-nj/` | 92 MB | 0 | LOW | Dormant |
| Freelance projects | `freelance-projects/` | 38 MB | 0 | LOW | 3 sub-projects w/ CLAUDE.md, dormant since ~Feb |
| Root marketing (modules/, kanban/, spec/, evidence/, google_ads_refined/, etc.) | root dirs | ~450 MB | ~0 | LOW | Sprint-2-era GTM scaffolding, mostly static |
| ~45 other `docs/` folders | `docs/*` | 1 KB–18 MB each | 0–4 files | LOW | Analyses, one-offs, archives |

---

## PetID Deep Dive

### Structure (`docs/pets_face_recon/`, 19 MB, 224 tracked files)

```
docs/pets_face_recon/
├── CLAUDE.md                      # 289-line project instructions (v1.1.0)
├── collaboration/                 # TRACEABILITY_MATRIX
├── config/  contracts/schemas/    # Pydantic/Zod contracts
├── docs/{agents_team_execution_plan, analysis, design, discovery, outreach}
├── evidence/sprint-{0,1,2,4,6}/
├── frontend/{frontend, public, src}   # React capture app + portal
├── kanban/  session-handoff/  spec/
├── ml/{calibration, spike}/       # petid_core.py, petid_datasets.py
├── modules/petid-{00-foundation, 00a-ci, 01…04, 06, 07, 08, spike-compute}/
├── scripts/  shared/lambda_utils/
├── tests/                         # 14 test files: unit, contracts, e2e
└── yolov5s.pt                     # 14.1 MB model weight, TRACKED in git
```

### Why it's the right pilot

- **Dormant**: last substantive commits 2026-06-04→06-09 (Sprint 5–7); nothing since. No in-flight work to disrupt.
- **Self-contained**: every tracked file sits under one path prefix — feature branches scoped here cannot conflict with doscierge/agent work.
- **Verifiable**: a real pytest suite (`tests/`, plus per-module tests; 169 passing at Sprint 7 per commit `df938be4`) gives PR reviewers something concrete to run.
- **Culturally close**: its CLAUDE.md Session End Checklist already mandates "changes committed (**conventional commits** with TDD evidence)" — the commit convention lands on prepared ground.

### What must change in PetID

1. **Reconcile the agent-teams file-ownership model.** `CLAUDE.md` §Execution Methodology defines Lead/Infrastructure/ML/Backend/Frontend/Quality teammates with **strict pre-scripted file ownership** — precisely the model `ACTIVE_WORK.md` replaces. Resolution: keep the table as a *role/skills guide* (it maps to the reference repo's optional **Tier 2**), and state explicitly that **runtime file coordination is via root `ACTIVE_WORK.md`** (Tier 1). Exact edit below.
2. **Add the Git workflow section** (branch naming, worktree, PR loop) — exact text below.
3. **Session checklists**: the Session Start checklist should add "read root `ACTIVE_WORK.md` + declare work"; Session End should add "PR created / ACTIVE_WORK row cleared".
4. Nothing in code needs to change. `yolov5s.pt` (14.1 MB) is fine to leave tracked for now (well under limits); consider Git LFS only if model weights multiply.

### Worktree setup for the pilot

Worktrees are **per-repo**, not per-folder — each one checks out all 10,700 tracked files (~240 MB, seconds to create, shares the 625 MB `.git`). That is acceptable, but **sparse-checkout keeps each session's blast radius honest**:

```bash
cd /home/ec2-user/environment/my_projects/aws_partner_analysis
WORKTREE_BASE="/home/ec2-user/environment/my_projects/aws_partner_analysis_worktrees"

git worktree add --no-checkout "$WORKTREE_BASE/session-a" master
cd "$WORKTREE_BASE/session-a"
git sparse-checkout set docs/pets_face_recon ACTIVE_WORK.md CLAUDE.md sync_github.sh
git checkout   # materializes only PetID + coordination files (~19 MB)
git checkout -b feature/petid-<short-desc>
```

Notes:
- `$WORKTREE_BASE` is a **sibling** of the repo, so worktrees are never accidentally tracked; no `.gitignore` entry needed.
- Worktrees share `.git`, so the PAT-embedded `origin` URL works from inside them unchanged; `git push origin <branch>` from a worktree just works.
- Sparse checkout also neutralizes the `add -A` monorepo-sweep risk: only PetID files exist in the worktree to be added.

---

## Pre-Configuration Checklist

Ordered; items 1–6 are required before the first PetID PR, 7–9 before propagation.

### Repo-wide (required for pilot)

- [ ] **1. Decide `master` vs `main`.** Recommendation: **keep `master`**, substitute `master` for `main` in all copied protocol text. Renaming (`git branch -m master main` + `git push origin main` + GitHub default-branch switch + delete `origin/master`) is clean on a solo repo but adds failure modes mid-adoption; defer it or do it as its own maintenance window. Everything below assumes `master`.
- [ ] **2. Replace `sync_github.sh`** with a branch-aware version. Start from `git_multi_agent_repo/sync_github.sh` and make four changes:
  - `GITHUB_REPO="gladiator9f/aws_partner_analysis"`; SSM param stays `/orchestraprime/github/pat` (already provisioned — no new parameter needed, unlike the reference repo's `pat_multi_agent_repo`).
  - `LOCAL_DIR="$(git rev-parse --show-toplevel)"` instead of a hardcoded path, so it runs correctly inside any worktree.
  - **Delete the `--force` fallback** (lines 86–88 of the reference script). `--force-with-lease` failing means *fetch and look*, never *overwrite*.
  - Replace `git add -A` with `git add -A -- "${SCOPE:-.}"` or simply require the caller to have staged/scoped changes; with sparse-checkout worktrees this is belt-and-suspenders.
- [ ] **3. Create `ACTIVE_WORK.md` at repo root** (commit to `master`). Same table as the reference repo **plus a Sub-Project column**:

  ```markdown
  | Session | Sub-Project | Branch | What I'm Doing | Key Files | Status |
  ```

- [ ] **4. Verify PAT permissions for `gh`.** The fine-grained PAT in `/orchestraprime/github/pat` was provisioned for Contents read/write (per `README_GITHUB_PAT.md`). PR create/review/merge additionally needs **Pull requests: Read and write** on `gladiator9f/aws_partner_analysis`. Test: `export GH_TOKEN=$(aws ssm get-parameter --name /orchestraprime/github/pat --with-decryption --query Parameter.Value --output text); gh pr list -R gladiator9f/aws_partner_analysis`. If it 403s, regenerate the PAT with the extra permission and rotate per `README_GITHUB_PAT.md`.
- [ ] **5. `.gitignore` additions** (root): `__pycache__/` and `*.pyc` — **40 `__pycache__` files are currently tracked**; add the ignore, then `git rm -r --cached` them in a `chore(repo):` commit. Optionally add `*.zip` going forward (a 22.5 MB zip is the largest tracked file).
- [ ] **6. GitHub repo settings**: confirm squash-merge is enabled (it is by default); optionally enable "automatically delete head branches". Branch protection on `master` (require PR) is the real enforcement for step 2's force-push risk — recommended once the pilot proves out, since it will also block the legacy direct-push sync habit.

### Per-sub-project (repeat at each propagation step)

- [ ] **7.** Add the Git-workflow section to the sub-project's CLAUDE.md (text below).
- [ ] **8.** Reconcile any sub-project-local coordination scheme (file-ownership tables, session registries) with root `ACTIVE_WORK.md` — PetID is the known case; `docs/doscierge/docs/agents_team_execution_plan/` likely has its own and must be checked before Phase 3.
- [ ] **9.** Confirm the sub-project has a verification command for PR review (PetID: `pytest docs/pets_face_recon/tests/`); document it in the CLAUDE.md section.

---

## Incremental CLAUDE.md Instructions

### A. Root `CLAUDE.md` — ADD this section (after "Session Start Checklist")

```markdown
## Git Workflow — Multi-Agent PR Protocol (MANDATORY)

This repo uses the multi-agent PR workflow. Full protocol:
/home/ec2-user/environment/my_projects/git_multi_agent_repo/CLAUDE.md (Tier 1).
Repo-specific deltas:

- **Default branch is `master`** (not `main`). Substitute accordingly in all
  protocol commands.
- **Never commit directly to `master`** except: ACTIVE_WORK.md claims, and
  root coordination files. Everything else goes through a feature branch + PR.
- **Worktrees**: create under
  `/home/ec2-user/environment/my_projects/aws_partner_analysis_worktrees/`
  with sparse-checkout scoped to your sub-project:
  `git worktree add --no-checkout <dir> master`, then
  `git sparse-checkout set docs/<sub-project> ACTIVE_WORK.md CLAUDE.md sync_github.sh`,
  then `git checkout && git checkout -b feature/<short-desc>`.
- **Branches**: `feature/<sub-project>-<short-desc>`, `bugfix/…`, `refactor/…`,
  `hotfix/…` — include the sub-project in the slug (e.g. `feature/petid-nose-crop`).
- **Commits**: conventional — `feat(petid): …`, `fix(doscierge): …`,
  `docs(nj-connect): …`. Scope = sub-project name.
- **Declare before branching**: add your row to root `ACTIVE_WORK.md` on
  `master` (Session | Sub-Project | Branch | What | Key Files | Status);
  remove it when your PR merges.
- **PRs**: `gh pr create` → cross-session review → `gh pr merge --squash
  --delete-branch`. Auth: `export GH_TOKEN=$(aws ssm get-parameter --name
  /orchestraprime/github/pat --with-decryption --query Parameter.Value
  --output text)`.
- **Push**: `./sync_github.sh push "<conventional message>"` (branch-aware; no
  force-push — if `--force-with-lease` fails, fetch and rebase, never override).
- **Legacy note**: the old whole-repo timestamp-sync habit
  ("Sync AWS Partner Analysis updates - <date>") is retired for sub-projects
  under this protocol. Adopted so far: **petid** (docs/pets_face_recon).
```

### B. `docs/pets_face_recon/CLAUDE.md` — three edits

**B1. ADD** (new section, place immediately before "## Execution Methodology"):

```markdown
## Git Workflow (ADOPTED 2026-08-XX — supersedes ad-hoc commits)

PetID follows the monorepo multi-agent PR protocol — see root CLAUDE.md
"Git Workflow" section. PetID specifics:

- Branch slugs: `feature/petid-<short-desc>`, `bugfix/petid-<short-desc>`
- Commit scope: `feat(petid): …`, `fix(petid): …`, `test(petid): …`
- Worktree sparse-checkout path: `docs/pets_face_recon`
- PR verification: `pytest docs/pets_face_recon/tests/` must pass before
  merge (reviewer runs it from the PR checkout)
- Runtime file coordination is root `ACTIVE_WORK.md` — declare files there,
  not via the teammate ownership table below
```

**B2. MODIFY** the Execution Methodology intro line. Current text (line ~187):

> Each sprint is executed by a **Lead + N Teammates** model with strict file isolation.

Replace with:

> Each sprint is executed by a **Lead + N Teammates** model. The table below
> defines *roles and default areas of responsibility* (Tier-2-style planning
> aid); **runtime file coordination is via root `ACTIVE_WORK.md` + PRs**, not
> pre-scripted ownership. Two teammates may touch the same area if both
> declare it and sequence via PR merge order.

**B3. MODIFY** Session Start Checklist (add item 7) and Session End Checklist (modify item 3):

```markdown
7. **Root `ACTIVE_WORK.md`** — check in-flight claims; declare yours before branching
```

Session End item 3, current: `**Git**: changes committed (conventional commits with TDD evidence).` → replace with:

```markdown
3. **Git**: changes committed on your feature branch (conventional commits,
   `feat(petid):` etc., with TDD evidence); PR created via `gh pr create`;
   your `ACTIVE_WORK.md` row updated or removed.
```

### C. Other sub-project CLAUDE.md files (at propagation time only)

Add one short block near the top of each (doscierge, slm_dm_regulatory_anda, agent, freelance-projects/*, etc.):

```markdown
## Git Workflow
This sub-project follows the monorepo multi-agent PR protocol — see root
CLAUDE.md "Git Workflow". Scope for commits/branches: `<sub-project-slug>`.
PR verification command: `<test/build command or "n/a — docs-only review">`.
```

Do **not** edit these until their propagation phase — premature instructions in an active area (doscierge) would collide with in-flight session habits.

---

## Rollout Plan

### Phase 0 — Pre-configuration (½ session, on `master` directly)

Items 1–6 of the checklist: sync-script replacement, `ACTIVE_WORK.md`, root CLAUDE.md section, `.gitignore` + `__pycache__` cleanup, PAT/`gh` verification. Commit as `chore(repo): adopt multi-agent PR workflow scaffolding`.

### Phase 1 — PetID pilot (1–2 weeks)

1. Apply CLAUDE.md edits B1–B3.
2. Run one **single-session** PR end-to-end first: worktree → branch → small real change (e.g. a docs or test improvement) → `gh pr create` → self-review → squash-merge. Proves PAT, script, and settings.
3. Then run a **two-session** exercise on PetID: independent tasks (e.g. Session A: `test(petid)` coverage gap; Session B: `docs(petid)` outreach update), both declaring in `ACTIVE_WORK.md`, cross-reviewing PRs.
4. Exit criteria: 3+ squash-merged PRs, one deliberate `ACTIVE_WORK.md` claim collision resolved by waiting/sequencing, zero force-pushes, `pytest` green on every merge.

### Phase 2 — Dormant/quiet sub-projects (as work resumes on them)

Order: `freelance-projects/*` → `docs/slm_dm_regulatory_anda` → `docs/nj-connect` → `docs/bio-nj` / `docs/reshoring_pharma_nj`. Each gets the short CLAUDE.md block (§C) the next time a session opens it — no big-bang edit of 16 files.

### Phase 3 — Hot areas (only after Phase 1 exit criteria met)

`docs/doscierge` and `docs/agent`. Precondition: check `docs/doscierge/docs/agents_team_execution_plan/` for its own coordination scheme and reconcile (as done for PetID). Time the switch to a sprint boundary (doscierge is mid-Sprint-8-era work; ANDA GATE-01 is ~2026-10-04 — switch at a lull, not mid-gate-push).

### Phase 4 — Enforcement + optional cleanup

- Enable branch protection on `master` (require PR; ACTIVE_WORK claims then move to tiny PRs or an allowed-actors exception — decide based on Phase 1 friction).
- Optional: `master` → `main` rename; optional: move PAT out of the remote URL to a credential helper.

---

## Risk Assessment

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|------------|
| 1 | **Legacy sync script force-pushes over a session's remote commits** — old habit or muscle memory runs the old `sync_github.sh` | Medium | **High** (lost pushed work) | Phase 0 replaces the script in place (same filename, safe behavior); `--force` fallback deleted; branch protection in Phase 4 makes it structurally impossible |
| 2 | **`git add -A` monorepo sweep** — a feature-branch commit accidentally includes unrelated sub-project changes left in a shared checkout | Medium | Medium (messy PRs, confusing squashes) | Sparse-checkout worktrees (only your sub-project's files exist); scoped `add` in the new script; main checkout reserved for `master` coordination only |
| 3 | **`master`/`main` mismatch** — copied protocol commands (`git worktree add … main`, `rebase origin/main`) fail or, worse, create a stray `main` branch | High if unaddressed | Low-Medium | Explicit "default branch is `master`" delta in root CLAUDE.md (§A); all rollout commands in this doc already use `master` |
| 4 | **PAT lacks PR permissions** — first `gh pr create` fails mid-demo | Medium | Low (blocks, doesn't break) | Checklist item 4 tests `gh pr list` in Phase 0; rotation procedure already documented in `README_GITHUB_PAT.md` |
| 5 | **PAT in cleartext in `.git/config`** (and in every worktree's shared config; also printed by `git remote -v`) | Existing condition | Medium (credential exposure) | Accept for pilot (single-user EC2 box, pattern predates this work); Phase 4: switch to credential helper / `GH_TOKEN`-only auth and scrub the remote URL |
| 6 | **ACTIVE_WORK.md contention** — every session commits claims to `master`; two sessions race | Medium | Low (trivial text conflict) | Protocol already covers it: pull before claim, rebase on reject; rows are single lines so conflicts auto-resolve or are one-line fixes |
| 7 | **Disrupting active doscierge/agent work** — a well-meaning session applies the new protocol to a hot area early | Medium | Medium | Root CLAUDE.md lists adopted sub-projects explicitly ("Adopted so far: petid"); Phase 3 gated on Phase 1 exit criteria + sprint boundary |
| 8 | **Squash-merge vs local history confusion** — after squash, feature branches show as diverged; sessions rebase wrongly | Medium | Low | Protocol mandates `--delete-branch` on merge + fresh branch per task from `origin/master`; never reuse a merged branch |
| 9 | **Disk pressure** — worktrees + 625 MB `.git` on a 71%-full 45 GB volume | Low | Low | Sparse worktrees are ~19 MB each for PetID; prune with `git worktree remove` at session end; monitor `df` |
| 10 | **PetID "dormant" assumption wrong** — user resumes PetID feature work mid-pilot outside the protocol | Low | Low | That's actually the pilot working as intended — route the resumed work through the first real feature PR |

### What could go wrong that this plan deliberately does NOT solve yet

- **CI on PRs**: there is no GitHub Actions setup; PR verification is reviewer-runs-pytest. Adding a minimal Actions workflow (pytest on `docs/pets_face_recon/**` path filter) is a natural Phase 2+ improvement, not a pilot prerequisite.
- **The 22 MB tracked binaries / 478 MB pack**: clone/CI cost, not a workflow blocker. Git LFS migration is out of scope.
- **16 CLAUDE.md files big-bang update**: intentionally avoided — propagation is lazy, per-sub-project, at next-touch time.

---

*Analysis performed against commit `7696ba7d` (master). All file paths, sizes, counts, and git facts verified by direct inspection on 2026-08-24.*
