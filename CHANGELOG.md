# Changelog

All notable changes to the KB Stack Monorepo will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2026-06-06

### Changed
- Bumped nested `kb-web` package version to `0.1.18` to incorporate virtual sites grouping, same-domain scraped link-ingestion confirmation modals, collapsible markdown content rendering, and sidebar layout updates.

## [0.1.1] - 2026-06-06

### Changed
- Configured Electron build configurations for `kb-clipboard`, `kb-rss`, and `kb-image` to output both portable and NSIS installer formats on Windows.
- Added native Windows `.ico` icons in `desktop/package.json` for all three Electron desktop apps to fix installer compile issues.
- Updated python `build.py` scripts to filter setup installers and only package the portable app.
- Updated python `build.py` scripts to dynamically resolve `uv` executable paths on systems where `uv` is not globally in `PATH`.
- Fixed CLI command bridges inside `kb-rss` and `kb-image` desktop apps to execute the globally installed CLI commands directly in production rather than executing `uv run`.
- Enabled `desktop_dist` assets packaging for `kb-image` by adding the `tool.uv.build-backend` config to its `pyproject.toml`.

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
