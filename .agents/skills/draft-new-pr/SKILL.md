---
name: draft-new-pr
description: Use this skill to create a git branch and a draft PR on GitHub for issues
---

# Draft New PR

Call the script [draft_new_pr.py](../../scripts/draft_new_pr.py) to check out a new branch, create an initial empty commit, push it to origin, create a draft PR on GitHub, and log details into `artifacts.db`.

## Usage

```shell
uv run scripts/draft_new_pr.py <REPO> <BRANCH_NAME> <ISSUE_IDS>
```

### Arguments
- `REPO`: The repository name, e.g., `kb-web`
- `BRANCH_NAME`: The name of the git branch to create (e.g. `feature/improve-ui`)
- `ISSUE_IDS`: A comma-separated list of database issue IDs that this PR addresses (e.g. `1` or `1,2`)

### Examples
```shell
uv run scripts/draft_new_pr.py kb-web "feature/fix-auth" "1"
uv run scripts/draft_new_pr.py kb-rss "feature/taste-refactor" "2,3"
```
