# KB Stack Monorepo (kb-mono)

This is the public monorepo for the `kb` (Knowledge-Base) suite of applications. The `kb` stack consists of localized, vertical-slice packages that import, model, and display knowledge for users and AI agents.

---

## Agent Initialization Rules

> [!IMPORTANT]
> **1. Understand Development Status on Initialization**
> Upon initializing a conversation in this workspace, the agent MUST read and understand the current development status of the `kb` packages by reading this `GEMINI.md` file and reviewing the public documentation under `docs/`.
>
> **2. Public Documentation and Secrets Policy**
> This repository is **PUBLIC**. All documentation under `docs/` is public. Do **NOT** document or commit any sensitive configuration details, private metadata, production API credentials, or personal system information in this repository.
>
> **3. local DB & CI/CD Tracking**
> The monorepo uses a local SQLite database `artifacts.db` to log and track development changes, draft issues, plans, and tasks. The agent must use the script tools in `scripts/` (e.g., `create_issue.py`, `draft_new_pr.py`, `publish_pr.py`) to keep the database synced with GitHub issues and PR status.
>
> **4. Gated Pre-Commit Checks**
> Before submitting changes for UAT or committing, the agent must run pre-commit checks (`scripts/pre_commit_checks.py`) to ensure code format/lint checks pass and all unit tests succeed.
>
> **5. Rules Evolution**
> The agent MUST always seek to distill new development, style, or architectural guidelines from user interactions. Propose these rules to the user, and upon approval, add them to this `GEMINI.md` initialization rules section.
>
> **6. README and CHANGELOG Update Policy**
> Before completing any issue/PR iteration, the agent must document all user-facing changes (new features, refactors, dependencies, fixes) in the root-level `CHANGELOG.md` under the appropriate release header, and keep the main `README.md` updated with any adjustments to submodule statuses, CLI commands, or prerequisites.

---

## Repo Structure

### `_tasks/`
This is where the user will place markdown files that describe tasks that have very specialized or long instructions for a task they want to achieve in the kb stack.

### `_pending_imports/`
This is where the user will place code references they want to use for a specific task; The user will specify which files and how to use them in the accompanying task request. **When the agent is done with a specific file(s), they should store then in the `artifacts` database attached to the user's request text for a given task.**

### `remotes/`
This is the primary directory where all active `kb` packages are cloned. Each subdirectory represents a standalone git repository.
- **Operations**: Agents review, refactor, and update these packages, maintaining standard build scripts, unit tests, and local documentation.
- **Repositories**:
  - [kb-core](remotes/kb-core)
  - [kb-clipboard](remotes/kb-clipboard)
  - [kb-image](remotes/kb-image)
  - [kb-rss](remotes/kb-rss)
  - [kb-web](remotes/kb-web)
  - [kb-wiki](remotes/kb-wiki)
  - [kb-network](remotes/kb-network)
  - [kb-network-agent](remotes/kb-network-agent)

### `docs/`
This directory contains internal **AGENT** documentation. Every development loop must be logged here by the active agent and registered inside the section below.
- [Guidelines for Agent Docs](file:///c:/Users/Will/Desktop/will_mono/docs/README.md)

`[AGENT DOCS SECTION]`
- [Repository Standards Update - May 26, 2026](docs/repo_standards_update_052626.md)
- [Repository Standards & Workflow Expansion - May 27, 2026](docs/repo_standards_and_workflow_expansion_052726.md)
- [Todo System Implementation - May 27, 2026](docs/todo_system_implementation_052726.md)
- [Python Server Template Update - May 27, 2026](docs/python_server_template_update_052726.md)
- [Create-Workflow Skill Implementation - May 27, 2026](docs/create_workflow_skill_implementation_052726.md)
- [Collect-User-Inputs Skill Implementation - May 28, 2026](docs/collect_user_inputs_skill_implementation_052826.md)
- [Remote Updates Workflow & CI Skill - May 29, 2026](docs/updating_remote_codebase_workflow_and_skill_052926.md)
- [Clipboard History Migration & Electron App UAT Standard - May 30, 2026](docs/clipboard_history_electron_migration_and_uat_standard_053026.md)
- [kb-rss Curation App Implementation - May 30, 2026](docs/kb_rss_implementation_053026.md)
- [kb-web Web Ingestion App Import - May 30, 2026](docs/kb_web_importer_migration_053026.md)
- [kb-web Settings, Curation & Browser Extension - May 31, 2026](docs/kb_web_enrichment_and_browser_extension_053126.md)
- [kb-web Service & Deployment Fixes - May 31, 2026](docs/kb_web_service_and_deployment_fixes_053126.md)
- [Remotes Curation & Branding Updates - June 1, 2026](docs/remotes_curation_and_branding_updates_060126.md)
- [Git Submodules Setup & Maintenance - June 3, 2026](docs/git_submodules_setup_060326.md)
- [KB Stack Cleanup and Normalization - June 4, 2026](docs/cleanup_and_normalization_060426.md)
- [KB Web Feature Updates (PWA, YouTube, Embeddings, MCP) - June 4, 2026](docs/feature_updates_to_kb_web_060426.md)
- [KB Repo and KB Vault Package Creation - June 5, 2026](docs/kb_repo_and_kb_vault_package_creation_060526.md)
- [YouTube Tooling and Warning Fixes - June 5, 2026](docs/youtube_tooling_and_warning_fixes_060526.md)
- [Stateless Authentication & Concurrency Refactor - June 5, 2026](docs/stateless_auth_refactor_and_concurrency_testing_060526.md)
- [KB Devblog Package Creation - June 5, 2026](docs/kb_devblog_package_creation_060526.md)
- [kb-core Overview - May 29, 2026](docs/kb_core_overview.md)
- [kb-clipboard Overview - June 6, 2026](docs/kb_clipboard_overview.md)
- [kb-image Overview - May 29, 2026](docs/kb_image_overview.md)
- [kb-web Overview - May 31, 2026](docs/kb_web_overview.md)
- [kb-rss Walkthrough - May 30, 2026](docs/kb_rss-walkthrough.md)
- [kb-web Importer Walkthrough - May 30, 2026](docs/kb_web-walkthrough.md)
- [kb-web Settings & Extension Walkthrough - May 31, 2026](docs/kb_web-walkthrough-pt2.md)
- [kb-web Virtual Sites & Links Integration - June 6, 2026](docs/kb_web_virtual_sites_and_links_v5_060626.md)
- [kb-web Virtual Sites & Links Layout Adjustment - June 7, 2026](docs/kb_web_virtual_sites_and_links_v5_adjustment_060726.md)
`[/AGENT DOCS SECTION]`

### `scripts/`
This directory houses scripts for tasks of this monorepo, such as initializing runs, managing git commits, and setting up remote updates. Scripts are executed using `uv run scripts/<script_name>.py [args]` or PowerShell equivalents.

---

## System Folders and Files

- `_pending_imports/` - Directory holding code waiting to be refactored and migrated into `remotes/`.
- `_tasks/` - Directory used by the user to house change-requests; these are markdown files containing instructions about proposed changes to a project. The user will specify a file here for the agent to use as a guide for a given task.
- `artifacts.db` - SQLite database containing the tables (`remotes_index`, `changes`, `issues`, `plans`, `tasks`) for tracking CI/CD development, user requests, and agent actions.
- `_new_commit_id` - File holding the commit ID generated by `scripts/setup_commit_workflow.py`.
- `_new_import_id` - File holding the import ID generated by `scripts/setup_import_workflow.py`.
- `_new_remote_update_id` - File holding the update ID generated by `scripts/setup_remote_update_workflow.py`.
- `scratch/` - Space for temporary scratchpad code and manual backups.
- `_todos` - File holding active tasks and database states for developer reminders.
- `.templates/` - Scaffolding files for Python server services.

---

## Agent Skills
Specific agent skills are available in the `.agents/skills/` directory to help automate development and maintain the database:
- `list-remotes`: Uses `scripts/list_remotes.py` to view available packages in the monorepo.
- `create-issue`: Uses `scripts/create_issue.py` to draft issues using the `gh` CLI and save them in `artifacts.db`.
- `view-issues`: Uses `scripts/view_issues.py` to list and filter logged issues.
- `draft-new-pr`: Uses `scripts/draft_new_pr.py` to check out branch, make initial commit, and create draft PR.
- `publish-pr`: Uses `scripts/publish_pr.py` to push changes and mark the draft PR as ready on GitHub.
- `get-current-statuses`: Uses `scripts/get_current_statuses.py` to view checked-out branches and modified files.
- `get-commit-history`: Uses `scripts/get_commit_history.py` to view recent submodule commit messages.
- `get-diffs`: Uses `scripts/get_diffs.py` to show colorized diffs of working tree changes.
- `pre-commit-checks`: Uses `scripts/pre_commit_checks.py` to validate package tests, lints, and changelogs.
- `add-agent-note` / `search-agent-notes`: Uses `scripts/add_agent_note.py` and `scripts/search_agent_notes.py` to record/search agent memories.
- `document-code-issue-and-fix`: Uses `scripts/document_code_issue_and_fix.py` to log resolved bugs.

---

## Python Standards

All python packages and tools in this workspace utilize `uv` for dependency management and execution.

### Data Modeling
- **sqlite-utils**: Preferred database choice for local, self-contained `kb` data stores (e.g. `~/.kb/kb.db`). Integrates directly with Pydantic via `model_dump()`.
- **pydantic**: Used for robust validation, parsing, and type safety across all database APIs.
- **SQLAlchemy ORM + Postgres**: Choice for shared multi-host network applications where postgres redundancy is required.

### Web Frameworks
- **FastAPI**: Lightweight backend server framework (fully compatible with Pydantic payloads).

### CLI Applications
- **Typer**: Console application framework. Combined with `rich.console.Console` for interactive output.

### Web Interactions
- **httpx**: Library for asynchronous HTTP clients and web scrapers.

---

## User Build and Deployment Standards / Preferences

- **Typer CLI + Daemon launchers**: Python CLIs must support daemonizing background processes (e.g. `start` command launching background loops via subprocess without leaving open terminals, using `pythonw` on Windows).
- **TypeScript / Javascript**: Standard runtime is `bun`. React + Electron-builder for GUI packaging.

---

## User Style Preferences

- **Color Palette**: Solarized light (`solarized-light`) with custom `retro-dark` support.
  - Background: Creamy `#F4EFEA` or solarized `#fdf6e3`. Accent orange (`#cb4b16`) and turquoise (`#2aa198`).
- **Layouts**: Pinned menus, minimalist elements, and zoom compatibility (comfortable at 70% scaling on wide screens).
- **Inspirations**: Earth-toned retro aesthetics reminiscent of the 1930s WPA and 2010s National Park Service posters.

---

## Package Development Status

| Package | Purpose | Status |
|---|---|---|
| `kb-core` | Shared configuration and notifier utils. | Stable |
| `kb-clipboard` | Clipboard synchronizer service and Electron GUI. | Complete. Background detacher daemon implemented. |
| `kb-image` | Metadata extractor and image indexing app. | Complete. Background detacher daemon implemented. |
| `kb-rss` | AI Taste agent, curation catalog, and Electron GUI. | Complete. Handles SQLite sorting and scraper API integration. |
| `kb-web` | Web curation and browser extensions portal. | Complete. Exposes REST API ingestion and admin portals. |
| `kb-wiki` | Collator and documentation compiler website. | Complete. Spawns static compilers and server routes. |
| `kb-repo` | Repository scanner and file watcher daemon. | Complete. Background detacher daemon implemented. |
| `kb-vault` | Obsidian vault markdown scanner and indexer. | Complete. CLI indexer fully functional. |
| `kb-network` | Host network supervisor and monitor service. | Spec Defined. Inactive / Pending development. |
| `kb-network-agent` | Host daemon for network monitoring. | Spec Defined. Inactive / Pending development. |
| `kb-devblog` | Technical devblog draft management and SQLite catalog. | Stable |
