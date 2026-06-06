---
name: get-commit-history
description: Use this skill to view recent commit logs for managed kb packages
---

# Get Commit History

Call the script [get_commit_history.py](../../scripts/get_commit_history.py) to view git commit history for submodules.

## Usage

```shell
uv run scripts/get_commit_history.py [OPTIONS]
```

### Options
- `--repo`, `-r`: The repository name, e.g., `kb-web`. If not provided, lists commits for all packages.
- `--limit`, `-n`: Number of commits to show (default: 5).

### Examples
```shell
uv run scripts/get_commit_history.py
uv run scripts/get_commit_history.py --repo kb-web --limit 10
```
