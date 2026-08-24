# git_multi_agent_repo

A Python project built and maintained by multiple Claude Code sessions working in parallel via Git branches and Pull Requests.

## Project Structure

```
src/
├── config/
│   └── settings.py        # Settings dataclass, env var loading
├── models/
│   └── task.py             # Task/TaskStatus dataclasses, factory
└── utils/
    ├── string_helpers.py   # slugify, truncate, sanitize_html
    └── date_helpers.py     # format_date, parse_date, date_diff_days
tests/
├── test_settings.py
├── test_task_model.py
├── test_string_helpers.py
└── test_date_helpers.py
```

## Setup

```bash
python3 -m pip install -r requirements.txt
```

## Usage

```python
from src.utils.string_helpers import slugify, truncate, sanitize_html
from src.utils.date_helpers import format_date, parse_date, date_diff_days
from src.config.settings import load_settings
from src.models.task import create_task, TaskStatus

# String helpers
slugify("Hello World!")          # "hello-world"
truncate("long text...", 8)      # "long..."
sanitize_html("<b>bold</b>")     # "bold"

# Date helpers
from datetime import datetime
format_date(datetime(2026, 8, 24))            # "2026-08-24"
parse_date("2026-08-24")                       # datetime(2026, 8, 24)
date_diff_days(datetime(2026, 8, 1), datetime(2026, 8, 24))  # 23

# Configuration (reads APP_NAME, APP_VERSION, DEBUG, LOG_LEVEL from env)
settings = load_settings()

# Task model
task = create_task("Fix bug", "Edge case in parser", assignee="Alice")
task.status = TaskStatus.IN_PROGRESS
```

## Running Tests

```bash
python3 -m pytest tests/ -v
```

## Multi-Agent Workflow

This repo uses a Git-based coordination protocol for parallel Claude Code sessions. See [`CLAUDE.md`](CLAUDE.md) for the full protocol. The key idea:

- Each session works in its own **git worktree** (isolated checkout)
- Sessions declare work in `ACTIVE_WORK.md` before branching
- One PR per feature, cross-session review, squash-merge to main
- Conflicts resolved by rebase — first merged wins

To start a multi-agent session:

1. Open 2+ terminals in this directory
2. Run `claude` in each
3. Tell each session its ID ("You are Session A / B")
4. Each reads `CLAUDE.md` and follows the Tier 1 protocol
