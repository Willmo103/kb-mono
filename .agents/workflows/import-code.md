---
description: Import the specified code from the `_pending_imports/` folder as a `kb` application package inside `remotes/`
---

# Import Code

## Context

This is the prescribed process for how the user expects code to be migrated into this repository, and it consists of 6 *distinct* parts:
1. **Plan**: Fully examine the codebase and gain an understanding of what *should* be included in a ported version under the target directory `remotes/kb-<package_name>`. Create a `plan_1.md` file in the new import directory that outlines the plan.
2. **Setup**: Initialize the codebase location and create a `uv` environment.
3. **Configuration**: Migrate configuration code and write integration tests.
4. **Data Models**: Migrate data sources and models (SQLite/sqlite-utils/Postgres) and write tests.
5. **Features**: Migrate endpoints, logic, and features module-by-module with tests.
6. **Build & Release**: Ensure all unit tests pass, prepare the build pipeline, and document the package setup.

---

## Setup

1. Before starting, locate the source folder under `_pending_imports/` and ensure that it exists. If not, stop and inform the user.
2. Run the setup script to initialize the run ID and artifact directory:
   ```shell
   uv run scripts/setup_import_workflow.py
   ```
   *Note: Use the generated `$import_id` and artifact directory path (`artifacts/imports/$import_id/`) in the following steps.*

---

## Process

### 1. Plan

Using tools, examine the contents of the incoming codebase, keeping the following questions in mind:
1. Given the target `kb` package layout, how best should this code be organized inside the new `remotes/kb-<package_name>` directory? (Remember: we are not married to the incoming code's layout, only its functionality).
2. What about the incoming code can be improved or cleaned up in the porting process?
3. How should this code be built for distribution?
4. What coding standards can be distilled from this codebase, and how do they align with the user's coding standards? (Refer to [GEMINI.md](file:///c:/Users/Will/Desktop/will_mono/GEMINI.md)).
5. What new functionalities can be added or improved?

> [!IMPORTANT]
> **Interactive Requirement Alignment**:
> The agent MUST run or recommend the user run the `/grill-me` slash command to align on technical requirements, design decisions, and specific configurations needed for the package being imported.

Create a plan outlining these details, save it as `artifacts/imports/$import_id/plan_1.md`, and obtain user approval. If edits are made based on user feedback, save them sequentially as `plan_2.md`, etc.

### 2. Identify and Recreate Environment

Using the approved plan as a guide, initialize the directory at `remotes/kb-<package_name>`, create a `pyproject.toml` (or standard config), and run `uv sync` to configure the virtual environment.

### 3. Identify and Recreate Configuration

Migrate configuration helpers and settings (subclassing `kb_core.config.Config` if applicable). Write tests confirming configurations are loaded properly and defaults are parsed.

### 4. Identify Datasources and Models

Migrate the database schemas and data models (using `sqlite-utils` for local SQLite stores, or `pydantic` models). Write unit tests covering database creations, reads, and writes.

### 5. Identify and Recreate Features

Migrate core logic, CLI commands (Typer), FastAPI server endpoints, templates, and UI files. Add unit tests for each module as you migrate them to ensure no regressions are introduced.

### 6. Build, Test, and Document

1. Write a root-level `build.py` script performing:
   - Dependency sync.
   - Test execution (`uv run pytest`).
   - Distribution compile (`uv build`).
2. Run the test suite and verify it passes 100%.
3. Update the package documentation (`README.md`, docstrings, and registering walkthroughs in `remotes/GEMINI.md`).
4. Generate the final `walkthrough.md` log inside `artifacts/imports/$import_id/`.

---

## Success Criteria

- A plan is written, approved, and tracked with version history inside `artifacts/imports/$import_id/`.
- The code is fully migrated into `remotes/kb-<package_name>` and brought to the `kb` ecosystem standards.
- A comprehensive unit test suite passes 100%.
- An automated `build.py` script executes successfully.
- Walkthrough log is created, and the documentation in `remotes/GEMINI.md` is updated.

---

## Abort/Error Handling

In case of failure or if the user requests to abort:
- Clean up any temporary files in the target directories.
- Log the reason in `artifacts/imports/$import_id/failure_log.md` and report it to the user.

**NOTE: AFTER all of reference code inside of `_pending_imports/` for this import *MUST* be cleaned up and removed, or else otherwise stored in documetation files inside of `docs/` as annotated code-blocks in markdown files *if* the code will be needed for future reference**
