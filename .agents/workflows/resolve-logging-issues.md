---
description: Read logs from local secrets config, verify task context via /grill-me, check out a new branch, resolve the issues, and run pre-commit checks.
---

# Resolve Logging Issues Workflow

## Context
This workflow outlines the step-by-step procedure for checking application log streams, identifying errors or database locks, aligning on the initiating task/incident details, and implementing standard fixes (such as transaction commits and Ollama parameters) inside a clean branch.

## Setup
1. Read the `KB_WEB_PROD_LOG_PATH` and `KB_WEB_PROD_DB_PATH` parameters from the local `.secrets` file located at the `kb-mono` root (`c:/Users/Will/Desktop/will_mono/remotes/kb-mono/.secrets`).
   *Example content:*
   ```ini
   KB_WEB_PROD_LOG_PATH=\\192.168.0.32\will-home\.kb\logs\kb-web.log
   KB_WEB_PROD_DB_PATH=\\192.168.0.32\will-home\.kb\kb.db
   ```

## Process

1. **Verify Context and Incident Tasks**:
   - Check the `_tasks/` directory or database tables in `artifacts.db` using `view-issues` to find any tasks matching the logged issues.
   - If the root cause, initiating incident, or user requirement is ambiguous, ask the user or suggest using the `/grill-me` slash command to align on goals and requirements.

2. **Examine Logs & Production Database**:
   - Open and inspect the log file path resolved from `KB_WEB_PROD_LOG_PATH`.
   - Identify active exceptions, stack traces, warning messages, or database concurrency/locking details.
   - Utilize the database located at `KB_WEB_PROD_DB_PATH` for inspecting current data states and debugging schema issues directly.

3. **Check Out a New Branch**:
   - Create and check out a clean git branch named `feature-<short-description>` using the `draft-new-pr` skill or standard git commands.

4. **Investigate Code and Implement Fixes**:
   - Analyze relevant source directories under the target repository (e.g. `remotes/kb-web/`).
   - Implement the necessary fixes. Standard patterns to verify/apply:
     - **Database Locking**: Ensure all raw database modification executions (e.g. `db.execute("UPDATE ...")`) are followed immediately by `db.conn.commit()` to release SQLite transaction locks.
     - **Ollama Model Prompts**: Verify that every `client.chat` or completion request carries the keyword argument `think=False` to prevent model reasoning delays.
     - **Programmatic Ingestion**: Ensure programmatic HTML/page imports correctly intercept YouTube links, scrape video transcripts/uploader metadata, and generate Gemma embeddings.
     - **Database backups BLOB formatting**: Convert bytes/BLOB columns to hex strings with a `hex:` prefix in JSON exports, and decode them back to binary bytes during imports.

5. **Write Verification Tests**:
   - Create new unit tests in the package's test suite (e.g., `tests/test_server.py`) to verify the fixes. Specifically cover:
     - Interception of YouTube page ingestion.
     - Binary bytes serialization and recovery in backups/restores.
   - Execute the unit test suite locally using `pytest` to make sure all tests pass.

6. **Execute Pre-commit Checks**:
   - Run the pre-commit checks script using the `PYTHONUTF8=1` flag on Windows to avoid Unicode printing errors:
     ```shell
     $env:PYTHONUTF8=1; uv run scripts/pre_commit_checks.py <repo-name>
     ```
   - Verify that Ruff styling, formatting, and all unit tests pass cleanly.

7. **Update Documentation & Versioning**:
   - Document changes in `CHANGELOG.md` under a new release header.
   - Bump the version inside `pyproject.toml`.

8. **Submit Changes**:
   - Use the `publish-pr` skill or Git push to publish a draft pull request for user review.

## Success Criteria
- Logged errors/warnings are completely resolved.
- Comprehensive unit tests exist and the entire test suite passes 100%.
- Pre-commit checks complete successfully.
- Submodule version and `CHANGELOG.md` are updated.
- A draft pull request is published on GitHub.

## Abort/Error Handling
In case of failure or interruption:
- Clean up any generated temporary files.
- Revert modified source files in the submodules using `git restore`.
- Document any blocks or findings to the user.
