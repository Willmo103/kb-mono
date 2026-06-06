---
name: document-code-issue-and-fix
description: Use this skill to document code bugs and their corresponding fixes in artifacts.db
---

# Document Code Issue and Fix

Call the script [document_code_issue_and_fix.py](../../scripts/document_code_issue_and_fix.py) to save a structured log of a code bug and its fix in `artifacts.db`.

## Usage

```shell
uv run scripts/document_code_issue_and_fix.py <ISSUE> <DESCRIPTION> [OPTIONS]
```

### Arguments
- `ISSUE`: A short summary of the code problem.
- `DESCRIPTION`: A detailed description of the bug or code symptom.

### Options
- `--before`, `-b`: A code snippet representing the broken code, OR a local file path containing the broken code.
- `--after`, `-a`: A code snippet representing the corrected code, OR a local file path containing the corrected code.
- `--explanation`, `-e`: Summary of why this change fixed the bug.

### Examples
```shell
uv run scripts/document_code_issue_and_fix.py "JSON decoding failure on empty state" "Empty state file caused parser crash because it tried to load empty string." --before "data = json.loads(text)" --after "data = json.loads(text or '{}')" --explanation "Ensured json parser receives a fallback string instead of crashing."
```
