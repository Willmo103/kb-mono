---
name: pre-commit-checks
description: Use this skill to run pre-commit checks on a submodule repository
---

# Pre-Commit Checks

Call the script [pre_commit_checks.py](../../scripts/pre_commit_checks.py) to check changelog updates, lint/format rules, and pytest test suite execution status for a package.

## Usage

```shell
uv run scripts/pre_commit_checks.py <REPO>
```

### Arguments
- `REPO`: The repository name, e.g., `kb-web`

### Examples
```shell
uv run scripts/pre_commit_checks.py kb-web
```
