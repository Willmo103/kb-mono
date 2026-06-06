---
name: add-agent-note
description: Use this skill to save a developer or agent note to artifacts.db
---

# Add Agent Note

Call the script [add_agent_note.py](../../scripts/add_agent_note.py) to save a development note, quirk, pattern, or reminder into `artifacts.db`.

## Usage

```shell
uv run scripts/add_agent_note.py <TITLE> <CONTENT> [OPTIONS]
```

### Arguments
- `TITLE`: The summary title of the note
- `CONTENT`: The detailed body (can be Markdown formatted text)

### Options
- `--tags`, `-t`: Comma-separated tags to label/categorize the note (e.g. `electron,ci,sqlite`)

### Examples
```shell
uv run scripts/add_agent_note.py "Obsidian watch issue" "Watcher daemon must run in background using pythonw on Windows to prevent CLI console locking." --tags "windows,kb-vault,watcher"
```
