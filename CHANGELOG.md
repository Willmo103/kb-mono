# Changelog

All notable changes to the KB Stack Monorepo will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-06-06

### Added
- Initialized `kb-mono` repository grouping `kb-*` packages as submodules under `remotes/`.
- Created local SQLite `artifacts.db` schema (`remotes_index`, `changes`, `issues`, `plans`, `tasks`, `agent_notes`, `code_fixes`) for robust local development loops.
- Implemented script-based development tooling in `scripts/`:
  - `populate_packages.py`: Scans and registers packages.
  - `list_remotes.py` / `view_issues.py`: Query commands.
  - `create_issue.py` / `draft_new_pr.py` / `publish_pr.py`: GitHub integrations.
  - `get_current_statuses.py` / `get_commit_history.py` / `get_diffs.py`: Git query helpers.
  - `pre_commit_checks.py`: Formatting (Ruff), testing (pytest), and changelog validation gates.
  - `add_agent_note.py` / `search_agent_notes.py` / `document_code_issue_and_fix.py`: Developer memories.
- Copied and updated `.agents` folder containing skills and workflows adapted for the new parent monorepo structure.
- Migrated 19 documentation logs from `will_mono` docs, sanitizing local absolute paths into relative markdown routes.
- Wrote public monorepo `README.md` and initial `CHANGELOG.md`.
