---
name: view-issues
description: Use this skill to view logged issues in artifacts.db
---

# View Issues

Call the script [view_issues.py](../../scripts/view_issues.py) to list and filter logged issues in the `kb-mono` repository.

## Usage

```shell
uv run scripts/view_issues.py [OPTIONS]
```

### Options
- `--repo`, `-r`: Filter issues by a specific repository name (e.g., `kb-web`).
- `--label`, `-l`: Filter issues by label (e.g., `bug` or `feature`).

### Examples
```shell
uv run scripts/view_issues.py
uv run scripts/view_issues.py --repo kb-web
uv run scripts/view_issues.py --repo kb-rss --label bug
```
