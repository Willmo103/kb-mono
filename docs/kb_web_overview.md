# kb-web Overview

`kb-web` is the web ingestion and dashboard portal for the `kb` (Knowledge-Base) ecosystem. It provides a FastAPI-based server, template rendering for feeds and settings, versioning of re-fetched pages, and integration with Chrome Extensions and Ollama LLM agents to automatically summarize and tag scraped content.

## Module Structure

The package is structured as a standalone python package with the following modules:

- **[config.py](../remotes/kb-web/src/kb_web/config.py)**: Configures LLM endpoint variables (`KB_OLLAMA_HOST`, `KB_OLLAMA_MODEL`, `KB_OLLAMA_EMBEDDING_MODEL`), Gotify notifications (`GOTIFY_URL`, `GOTIFY_TOKEN`), client API authentication keys (`KB_API_KEY`), and custom prompts. Supports persisting modifications to a local JSON configuration file.
- **[db.py](../remotes/kb-web/src/kb_web/db.py)**: Manages sqlite database interactions and schema upgrades. Automatically verifies table columns and applies migrations to support `title` and `tags` columns, a separate `page_versions` table for historical content snapshots, and an `article_embeddings` table for semantic similarities.
- **[models.py](../remotes/kb-web/src/kb_web/models.py)**: Holds Pydantic validation structures, defining validation logic for parsed URL targets and ingested HTML pages.
- **[server.py](../remotes/kb-web/src/kb_web/server.py)**: Implements all FastAPI handlers. Handles public feeds routing, admin dashboards, manual tag/wiki regeneration requests, source URL re-fetching and snapshotting, security password updating, direct web ingestion, URL copy-paste parsing, tags list rendering, YouTube transcripts extraction (via `youtube-transcript-api`/`yt-dlp`), and semantic similarity calculations.
- **[mcp_server.py](../remotes/kb-web/src/kb_web/mcp_server.py)**: Exposes a stdio-based Model Context Protocol (MCP) server providing agents with tools to list, query, search, and find similar wiki entries in the database.
- **[cli.py](../remotes/kb-web/src/kb_web/cli.py)**: Exposes a Typer command-line application structure to start/run the web application server (`kb-web serve`) and run the MCP server (`kb-web mcp`).

## Browser Extension

- **[browser_extension/](../remotes/kb-web/browser_extension/)**: Contains a Manifest V3 browser extension. Features options page configurations and a background script that posts raw tab HTML contents to the ingestion API using the browser extension API.

## Systemd & Service Scripts

- **[kb-web.service](../remotes/kb-web/kb-web.service)**: systemd unit file templated to run the web server on production Linux environments. It runs as user `will` under `/srv/kb-web`, loading an optional `.env` file and calling the compiled `.venv` python binary directly.
- **[scripts/install_service.sh](../remotes/kb-web/scripts/install_service.sh)**: Automatically updates, copies, enables, and registers the systemd unit file. Runs `uv sync` to build the local virtualenv automatically if missing.
- **[scripts/manage.sh](../remotes/kb-web/scripts/manage.sh)**: Simple CLI utility wrapper to start, stop, restart, check status, and tail systemd service logs.

## Build & Testing

The package includes:
- **[build.py](../remotes/kb-web/build.py)**: Automated script to synchronize dependencies (`uv sync`), run the test suite (`uv run pytest`), and build distribution packages (`uv build`).
- **tests/**: pytest unit tests verifying routing, authentication protection, page deletions, re-fetching/snapshot versioning, administrative configurations, dirty URL extraction, tag listing, and YouTube transcript ingestion.
