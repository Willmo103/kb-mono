---
name: search-agent-notes
description: Use this skill to query and view developer notes stored in artifacts.db
---

# Search Agent Notes

Call the script [search_agent_notes.py](../../scripts/search_agent_notes.py) to search through saved notes in `artifacts.db` using query strings or tags.

## Usage

```shell
uv run scripts/search_agent_notes.py [QUERY] [OPTIONS]
```

### Arguments
- `QUERY`: (Optional) Text to search for in titles or note contents.

### Options
- `--tag`, `-t`: Filter results by a specific tag.

### Examples
```shell
uv run scripts/search_agent_notes.py
uv run scripts/search_agent_notes.py "electron"
uv run scripts/search_agent_notes.py --tag windows
```
