# Codebase Migration - kb_web_importer to remotes/kb-web
**Date:** May 30, 2026  
**Agent ID:** Antigravity

This document details the migration of the `kb_web_importer` code repository from the `_pending_imports/` staging directory into a fully structured, version-controlled Python package under `remotes/kb-web`.

---

## 1. Overview & Objectives

The primary goal was to convert a standalone FastAPI script (`server.py` and templates) into a clean, deployable python library package complying with repository guidelines:
- **Core Library Integration**: Reads configuration properties and initializes database references using `kb-core` structures.
- **Shared Storage**: Scrapes and stores page profiles to the shared database located at `~/.kb/kb.db` (instead of local project files).
- **Typer Command Launcher**: Exposes a CLI entrypoint for running the web service.
- **Production Package Layout**: Packages static resources (Jinja2 HTML and text templates) within the library namespace.
- **Production Deployment Flow**: Integrates systemd configurations for running as a daemon on the target server.

---

## 2. Package Architecture

The target repository structure inside `remotes/kb-web` is laid out as follows:

```
remotes/kb-web/
├── pyproject.toml         # Package dependency config (fastapi, typer, kb-core, markdown, etc.)
├── kb-web.service         # Systemd service unit template for Linux systems
├── README.md              # Project manual and instruction guide
├── src/
│   └── kb_web/
│       ├── __init__.py    # CLI entrypoint exposure (main() hook)
│       ├── config.py      # App-specific configs inheriting from kb_core.config.Config
│       ├── db.py          # Database setup and schema initialization helper
│       ├── models.py      # Pydantic schemas (ParsedUrl and HTMLPage) with link resolution
│       ├── server.py      # FastAPI application endpoints, auth handlers, and background tasks
│       ├── cli.py         # Typer CLI application (defines 'serve' command)
│       └── templates/     # Jinja2 HTML page render templates
└── tests/
    └── test_server.py     # Isolated pytest unit and integration test suite
```

---

## 3. Key Design Implementations

### A. Configuration & Storage Integration (`config.py` & `db.py`)
The `Config` class inherits from `kb_core.config.Config`. It resolves parameters in the following priority order:
1. Environment variables (`KB_PASSWORD`, `KB_OLLAMA_HOST`, `GOTIFY_URL`, `GOTIFY_TOKEN`).
2. Config file attributes (stored at `~/.kb/configs/kb-web.json`).
3. Core fallback defaults (`admin123` for passwords, and `http://localhost:11434` for Ollama).

Database tables are initialized using `sqlite-utils` inside the shared SQLite file at `~/.kb/kb.db` (evading local file storage locks or isolation).

### B. Template Resolution in Packaged Libraries (`server.py`)
To enable packaging the application as a wheel and running it anywhere, templates are loaded using Jinja2's `PackageLoader`:
```python
_jinja_env = jinja2.Environment(loader=jinja2.PackageLoader("kb_web", "templates"))
```
This ensures templates compile correctly from the site-packages namespace without relying on relative path resolution.

### C. Route Guard & Webhook Responses
FastAPI endpoint response models are configured with `response_model=None` on union-returning endpoints to allow returning either `HTMLResponse`, `RedirectResponse`, or `StreamingResponse` without failing Pydantic validation checks.

---

## 4. Testing & Verification

Automated testing resides in `tests/test_server.py`. It uses a temporary folder path override for the database to ensure test operations are isolated from production user records.
- Config validation, Pydantic relative URL resolvers, and FastAPI login authentication flow tests run via:
```bash
uv run pytest
```

---

## 5. Deployment Framework

Deployment is executed via Git on the remote Linux host under `/srv/kb-web/`:
1. **Repository Checkout**: The target repository is cloned to `/srv/kb-web` and owned by the host user (`will`).
2. **Virtual Environment**: A Python venv is initialized locally inside `/srv/kb-web/`, and the package is installed: `.venv/bin/pip install .`.
3. **Daemonization**: A systemd service file `kb-web.service` is copied to `/etc/systemd/system/` and runs the server using `.venv/bin/kb-web serve` under the local user context.
