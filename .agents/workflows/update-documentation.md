---
description: Process for updating documentation and changelogs across the kb packages and agent workspace
---

# Documentation Update Procedure

## Context
Every development loop requires maintaining accurate documentation. This workflow outlines the multi-tiered process for checking differences, identifying affected `kb` packages, updating local and public documents, recompiling the documentation wiki, and logging agent history.

---

## Setup

1. Run the setup script to initialize the commit run ID and artifact directory:
   ```shell
   uv run scripts/setup_commit_workflow.py
   ```
   *Note: Use the generated `$commit_id` and artifact directory path (`artifacts/changelog/$commit_id/`) in the following steps.*

---

## Process

### Step 1. Examine Git Diffs
Run `git diff` (or other status tools) to identify all file modifications. Save the list of changed files with a brief description of functional edits to `artifacts/changelog/$commit_id/git_diff.md`. If no functional or documentation changes exist, stop here.

### Step 2. Identify Affected Packages
Identify which of the `kb` packages in `remotes/` were changed. Create `artifacts/changelog/$commit_id/affected_packages.md` containing a list of the packages, their paths, and a file tree of their changed files.

### Step 3. Identify and Map Documentation Needs
For each affected package, identify what documentation needs to be added or revised. Create a checklist inside `artifacts/changelog/$commit_id/proposed_documentation_updates.md` using a table mapping files to their required docstring, comment, or README changes.

### Step 4. Execute the Tiered Documentation Update

Agents must execute updates across the following three tiers:

#### Tier 1: Local Package Level
- Update file-level and function/class-level docstrings in changed python files.
- Update `__init__.py` files if public modules or namespaces changed.
- Update the package-level `README.md` (e.g., `remotes/kb-<package>/README.md`) describing any new CLI flags, options, config keys, or schemas.

#### Tier 2: Public Wiki Level
- Update or create corresponding wiki pages under `remotes/kb-wiki/docs/kb-<package>/` or `kb-core.md` detailing user-facing setups, schemas, or guides.
- If new pages are added, register them in `TITLE_MAPPING` inside `remotes/kb-wiki/src/kb_wiki/compiler.py`.
- Navigate to `remotes/kb-wiki/` and recompile the documentation website to verify it builds successfully:
  ```shell
  uv run kb-wiki build
  ```
  Ensure there are no compiler errors or broken link warnings.

#### Tier 3: Agent Workspace Level
- Write a detailed agent log document in the workspace `docs/` folder (e.g., `docs/<change_desc>_<date>.md`).
- Register and link this new log in the `[AGENT DOCS SECTION]` of the root [GEMINI.md](file:///c:/Users/Will/Desktop/will_mono/GEMINI.md) file.
- Update the root `CHANGELOG.md` file by appending an entry summarizing the change under the generated `$commit_id`.

### Step 5. Draft Git Commit Message
Create `artifacts/changelog/$commit_id/draft_commit_msg.md` containing a structured Git commit message documenting all functional and documentation changes. Propose this to the user for git execution.

---

## Success Criteria

- All diffs are mapped, and affected packages are logged.
- Tier 1: Local docstrings and READMEs are fully updated.
- Tier 2: Public `kb-wiki` docs are written, mapped, and compiled cleanly with `kb-wiki build`.
- Tier 3: Agent log is written in `docs/`, registered in `GEMINI.md`, and the root `CHANGELOG.md` is updated.
- A draft commit message is created and ready for user stage/commit.
