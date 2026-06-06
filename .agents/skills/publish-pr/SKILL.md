---
name: publish-pr
description: Use this skill to commit changes, push, and publish draft PRs
---

# Publish PR

Call the script [publish_pr.py](../../scripts/publish_pr.py) to push the local changes of your branch to origin, mark the active draft Pull Request as ready on GitHub, and update local database status.

## Usage

```shell
uv run scripts/publish_pr.py <REPO> <CHANGELOG>
```

### Arguments
- `REPO`: The repository name, e.g., `kb-web`
- `CHANGELOG`: The changelog commit message detailing what was changed

### Examples
```shell
uv run scripts/publish_pr.py kb-web "Fixed the session timeout issues and refactored auth checks"
```
