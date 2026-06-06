---
name: create-issue
description: Use this skill to create a GitHub issue for a specific kb-package and log it in artifacts.db
---

# Create Issue

Call the script [create_issue.py](../../scripts/create_issue.py) to create a new issue for a specific remote repository. This will use the `gh` CLI to create the issue on GitHub and then log the issue details into `artifacts.db` in the `kb-mono` monorepo.

## Usage

```shell
uv run scripts/create_issue.py <REPO> <TITLE> <MESSAGE> [--label LABEL] [--project PROJECT] [--change-id ID]
```

### Arguments
- `REPO`: The repository name, e.g., `kb-web`
- `TITLE`: The title of the issue
- `MESSAGE`: The body description of the issue

### Options
- `--label`, `-l`: Label for the issue (default: "feature")
- `--project`, `-p`: GitHub project name to assign it to (default: "kb-mono CICD")
- `--change-id`, `-c`: (Optional) The `change_id` corresponding to the user request in `artifacts.db`

### Examples
```shell
uv run scripts/create_issue.py kb-web "Fix UI bug" "There is a bug in the settings page." --label "bug"
```
