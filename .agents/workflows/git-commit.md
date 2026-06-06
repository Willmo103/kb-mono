---
description: Execute a git commit
---

# Git Commit

## Setup

**If the `update-documentation` workflow has not been ran by the agent using this workflow, stop and run the `update-documentation` workflow**

1. Read the `_new_commit_id` file to get the current commit id ($commit_id)
2. Locate the artifact at the path `artifacts/changelog/$commit_id/draft_commit_msg.md. ensure it exists.

## Process

1. Run `black`
execute:
```shell
uv run black .
```
(Ignore any errors)

2. Inspect `.gitignore`

Inspect the `.gitignore` file and ensure that all files that *should* be ignoreed are ignored;
IF there are issues **STOP** and inform the user. Otherwise proceede.

3. Stage Changes
execute:
```shell
git stage .
```

4. Commit Changes

Commit all staged changes using the draft message as the commit message

```shell
git commit -a -m (here you can enter the message or pipe it from the file, if that has been *tested* to work before hand)
```
