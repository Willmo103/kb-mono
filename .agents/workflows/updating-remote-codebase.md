---
description: Process for updating a remote codebase under the remotes directory, standardizing code, adding testing, and updating documentation.
---

# Updating Remote Codebase Workflow

## Context
This workflow outlines the step-by-step process for reviewing and updating repositories cloned into the `remotes/` directory. Even though these repositories are remotes, they must be brought up to standard with testing, build scripts, and documentation, followed by a proposed commit message.

## Setup
1. Run the setup script to initialize the session and generate the run ID:
   ```shell
   uv run scripts/setup_remote_update_workflow.py
   ```
   *Note: Use the generated `$run_id` and artifact directory path (`artifacts/remote_updates/$run_id/`) in the following steps.*

## Process

1. **Examine and Analyze**:
   - Locate the target remote repository under the `remotes/` folder (e.g. `remotes/kb-core/`).
   - Analyze package configuration files (`pyproject.toml`, etc.), source directories, existing utility files, and module logic.
   - Identify bugs, code issues, or omissions.

2. **Update Agent Documentation Index**:
   - Create a limited, high-level overview document inside `remotes/docs/<package_name>_overview.md` describing modules, utilities, and build setup.
   - Update `remotes/GEMINI.md` under the `[AGENT_DOCUMENTATION_SECTION]` to reference the new file. Add a note indicating that remote documentation should be kept limited and updated regularly.

3. **Standardize Code and Implement Testing**:
   - Correct bugs in the code.
   - Add necessary dev packages (e.g. `pytest`, `pytest-mock` inside a `[dependency-groups]` or standard dependency specification) to the package setup (`pyproject.toml`).
   - Create a comprehensive set of unit tests in the `tests/` subdirectory of the remote project.
   - Create an automated build script (e.g., `build.py` at the remote root) that performs environment synchronization, executes tests, and builds packaging artifacts.

4. **Verify and Run Build Pipeline**:
   - Run the automated build script locally to verify that all tests pass and package distributions compile successfully.

5. **Draft Commit Message**:
   - Create a draft commit message file at `artifacts/remote_updates/$run_id/draft_commit_msg.md`.
   - Propose the commit message and changes to the user for staging and commit/push execution.

## Success Criteria
- Code bugs are resolved and codebase is brought to monorepo standard.
- The unit test suite exists and is 100% passing.
- An automated build script is present and executes cleanly.
- Overview document is created and registered in `remotes/GEMINI.md`.
- A draft commit message is generated in the session artifact folder.

## Abort/Error Handling
In case of workflow failure:
- Clean up any temporary files in the repository.
- Revert modified source files in the remote using `git restore` if requested by the user.
- Log failure reasons in `artifacts/remote_updates/$run_id/failure_log.md` and report them to the user.
