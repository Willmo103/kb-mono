# KB Stack Monorepo (kb-mono)

Welcome to the **KB Stack Monorepo**, the primary parent repository for tracking development, issues, CI/CD, and release management for the `kb` (Knowledge-Base) suite of applications.

The KB stack consists of vertical-slice, self-contained package modules designed to aggregate, index, query, and curate your personal knowledge graph, AI taste summaries, web bookmarks, and clipboard files.

## Monorepo Layout

- `remotes/`: Standalone submodules representing the distinct vertical slices of the KB ecosystem.
- `scripts/`: Automated development tooling for managing submodules, checking out branches, running local issue workflows, and pre-commit verification.
- `docs/`: Audited design documentation, walkthroughs, and repository history guides.
- `.agents/`: Automation skills and workflows for pair-programming agents and CI agents.

## Core Packages

| Package | Purpose | Status |
|---|---|---|
| [`kb-core`](remotes/kb-core) | Shared notification helpers (Gotify) and configuration schema. | Stable |
| [`kb-clipboard`](remotes/kb-clipboard) | Clipboard history manager with React/Electron GUI and local SQLite indexing. | Complete |
| [`kb-image`](remotes/kb-image) | Automated metadata extraction and image indexing service. | Complete |
| [`kb-rss`](remotes/kb-rss) | AI aggregator using local LLMs (Ollama) to curate feeds, with Electron React viewer. | Complete |
| [`kb-web`](remotes/kb-web) | Bookmark curation portal exposing REST APIs, FastAPI admin dashboard, and web extensions. | Complete |
| [`kb-wiki`](remotes/kb-wiki) | Document collator and compiler generating static HTML pages. | Stable |
| [`kb-repo`](remotes/kb-repo) | File watcher daemon and git status automation client. | Stable |
| [`kb-vault`](remotes/kb-vault) | Obsidian markdown indexing CLI suite. | Stable |
| [`kb-network`](remotes/kb-network) | Host network monitor and Ollama container status daemon. | Spec defined |
| [`kb-network-agent`](remotes/kb-network-agent) | Agent client executing status checks for `kb-network`. | Spec defined |

## Prerequisites and Installation

1. **Python Runtime**: Standardized on Python `3.13+` managed via [`uv`](https://github.com/astral-sh/uv).
2. **GitHub CLI**: `gh` command-line utility must be installed and authenticated to run PR/issue scripts.
3. **Node/Bun**: Frontend build layers require [`bun`](https://bun.sh/) for compiling UI packages.

To setup the packages:
```shell
git submodule update --init --recursive
uv sync
```

## Contributing and Branching Policy

This monorepo uses a local SQLite database (`artifacts.db`) to coordinate work:
1. **Create an Issue**: Log user requests locally and on GitHub using `uv run scripts/create_issue.py`.
2. **Draft a Branch**: Check out an issue branch and create a draft PR using `uv run scripts/draft_new_pr.py`.
3. **Validate Rules**: Run `uv run scripts/pre_commit_checks.py` before committing.
4. **Publish PR**: Push modifications and set the PR to ready using `uv run scripts/publish_pr.py`.
