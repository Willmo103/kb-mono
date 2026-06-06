---
name: get-diffs
description: Use this skill to view friendly, colorized git diffs of modified files in a kb package
---

# Get Diffs

Call the script [get_diffs.py](../../scripts/get_diffs.py) to view colorized git diff outputs in a specific sub-repository.

## Usage

```shell
uv run scripts/get_diffs.py <REPO> [OPTIONS]
```

### Arguments
- `REPO`: The repository name, e.g., `kb-web`

### Options
- `--cached`, `-c`: Show differences in staged changes (the code waiting to be committed).

### Examples
```shell
uv run scripts/get_diffs.py kb-web
uv run scripts/get_diffs.py kb-web --cached
```
