---
description: The prime development workflow detailing coding standards, skill selection, testing, documentation, and commit procedures for implementing changes.
---

# Implement Code Changes Workflow

## Context
This is the **prime development workflow** for proposing and implementing code modifications, new packages, bug fixes, or enhancements across the `kb` (Knowledge-Base) workspace. It standardizes the development cycle, guarantees compliance with repo-wide coding standards, outlines when to leverage specific skills, and defines testing, documentation, and staging requirements.

---

## Setup

1. **Initialize a Development Loop**:
   Before modifying any files, initialize a remote update workflow session to generate a unique run ID and output folder:
   ```powershell
   uv run scripts/setup_remote_update_workflow.py
   ```
   *Note: Save the generated `$run_id` and the artifact path (`artifacts/remote_updates/$run_id/`) for draft commits and logs.*

2. **Stage Development Loop Artifacts**:
   As per **Rule #4 of GEMINI.md**, initialize a version-controlled tracking directory under:
   `artifacts/development/<change_name>/<date>_<change_desc>/`
   Within this directory, create:
   - `tasks.md` (A markdown list containing checkboxes to track progress).
   - `plan_1.md` (The design document detailing the proposed modifications).

---

## Process

### 1. Repository Audit & Planning
1. **Audit Development Status**:
   Always read `remotes/GEMINI.md` and the package-specific walkthroughs inside `remotes/docs/` to verify the active package versions, architecture, and current status.
2. **Review Knowledge Items (KIs)**:
   Search `<appDataDir>\knowledge` for any snapshots/guides matching the task to avoid repeating past work or violating established constraints.
3. **Draft the Implementation Plan**:
   Write down the initial design in `plan_1.md` and populate the checklist in `tasks.md`.
   - *Iterative Feedback*: If the plan requires revision, save subsequent iterations sequentially (e.g. `plan_2.md`, `plan_3.md`) instead of overwriting previous plans.

### 2. Skill Selection Matrix
Depending on the task, consult and invoke the appropriate workspace skill:
- **`create-kb-electron-app-cli-package`**: Use this when bootstrapping a new vertical-slice package or modifying an existing package's React/Electron frontend and background Python watcher/daemon combination.
- **`create-python-github-workflow`**: Use this when setting up or standardizing GitHub Actions CI/CD workflows for testing, tagging, and creating GitHub releases.
- **`collect-user-inputs`**: Use this when you need to gather structured developer/user input through static HTML pages and store the feedback locally as JSON.
- **`personalize-writing`**: Use this when writing READMEs, package overviews, devblog posts, or documentation to align with the user's personal voice, tone, and formatting preferences.

### 3. Implementation Standards

#### 3.1 Python Backend Standards
- **Virtual Environments**: Always manage and synchronize packages inside the local `.venv` using `uv`.
- **CLI Commands**: CLI applications built with `typer` must expose:
  - `serve` (or `desktop`) to launch client apps.
  - `install` to add local binaries to User PATH and set up startup registry entries.
  - `update` to download prebuilt Electron portable binaries from GitHub Releases.
- **Background Processes**: Utilize pythonw (Windows) or fork processes to launch watchers/daemons as detached background scripts writing to PID files.
- **Data Stores**: Use `sqlite-utils` for localized local databases (`~/.kb/kb.db`) and `pydantic` for data validation/serialization.

#### 3.2 Electron/React Frontend Standards
- **Color Palette & Theme**: Rely exclusively on the curated Earth-toned retro solarized theme (solarized-light: background `#F4EFEA`, accent orange `#cb4b16`, turquoise `#2aa198`, retro-dark: background `#1C1917`).
- **Typography**: Load Google Fonts (e.g., Outfit or Inter) instead of system/browser defaults.
- **Tray Collapse & Restore**:
  - Intercept window `minimize` and `close` events to hide the app to the system tray (`event.preventDefault()`, `mainWindow.hide()`).
  - Set up double-click tray hooks to restore the window (`mainWindow.restore()`, `mainWindow.show()`).
  - Package `tray-icon.png` and `icon.png` inside `package.json`'s files array.

### 4. Testing & Verification
1. **Write Automated Tests**:
   Create comprehensive unit tests under the package's `tests/` directory leveraging `pytest` and `pytest-mock`.
2. **Run the Build pipeline**:
   Execute the package-level `build.py` script. The build script must:
   - Perform npm installation and build/package steps (`npm run dist` / `npm run build`).
   - Copy the compiled Electron portable binary to the Python source package directory (`src/<package_name>/desktop_dist/`).
   - Run python sync and pytest unit tests.
   - Compile python sdist/wheels via `uv build`.
3. **User Acceptance Testing (UAT)**:
   For visual client changes, run `npm run build` locally and instruct the user to test the GUI features before generating production wheel packages.

### 5. Documentation & Changelogs
1. **Maintain Changelogs**:
   Record all notable changes in `CHANGELOG.md` in keeping with the Keep a Changelog format.
2. **Register Package Overviews**:
   If modifying a package cloned under `remotes/`, write or update `remotes/docs/<package_name>_overview.md` describing modules, CLI flags, database integrations, and release configs. Register the new document in `remotes/GEMINI.md` under the `[AGENT_DOCUMENTATION_SECTION]`.

### 6. Staging and Commit Proposed Changes
1. **Draft Commit Message**:
   Write the commit summary inside `artifacts/remote_updates/$run_id/draft_commit_msg.md`.
2. **Commit Changes**:
   Stage changes and commit them locally in the respective packages and the root monorepo using the `/git-commit` workflow.
   - **DO NOT PUSH** submodules or monorepo changes to origin. The user will manually review local commits and push to GitHub, letting the GitHub Actions runner handle tag pushing and release creation.

---

## Success Criteria
- Code changes address the user request and adhere to style guidelines.
- Local `build.py` compiles Electron assets, passes `pytest` unit tests (100% pass rate), and successfully builds python wheels.
- `CHANGELOG.md` is updated to capture the exact version modifications.
- High-level package overview is updated/created and registered inside `remotes/GEMINI.md`.
- All development plans, checklists, and completion summaries are logged inside `artifacts/development/`.
- Submodule pointer updates and monorepo changes are staged and committed locally (working tree is clean).

---

## Abort/Error Handling
In the event of execution failure:
1. Log failure reasons inside `artifacts/remote_updates/$run_id/failure_log.md`.
2. Revert modified source files using `git restore .` in the submodules to avoid leaving a dirty working tree.
3. Clean up built build/dist/node_modules directories if necessary.
