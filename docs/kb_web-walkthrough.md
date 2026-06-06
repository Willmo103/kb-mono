# Walkthrough - `kb_web_importer` Migration to `remotes/kb-web`

I have successfully completed the migration and refactoring of the `kb_web_importer` FastAPI application into the target repository `remotes/kb-web` under the `/import-code` workflow. The migrated service integrates with the core `kb-core` library configuration, queries the shared database (`~/.kb/kb.db`), implements a Typer CLI command station, includes a robust test suite, and provides a systemd configuration.

---

## 1. Accomplished Work & File Layout

- **Configuration (`config.py`)**: Subclassed `kb_core.config.Config` to load environments (`KB_PASSWORD`, `KB_OLLAMA_HOST`, `GOTIFY_URL`, `GOTIFY_TOKEN`) and support configuration overrides via `~/.kb/configs/kb-web.json`.
- **Database Schema (`db.py`)**: Utilizes `config.get_db()` to interface with the shared database (`~/.kb/kb.db`). Implemented automatic initialization of the `fetched_pages` schema.
- **Pydantic Validation (`models.py`)**: Ports `ParsedUrl` and `HTMLPage` Pydantic models. Integrates validators resolving relative URLs to absolute links and parsing JSON keywords.
- **FastAPI Backend Server (`server.py`)**:
  - Implements route auth guards, login sessions, share target feeds, web ingestion, admin panels, database streaming exports, and websocket imports.
  - Resolves HTML/text templates using Jinja2 `PackageLoader("kb_web", "templates")` for seamless site-package packaging.
  - Invokes Ollama (`gemma4:latest`) for clean wiki extraction and updates Gotify push alerts using `kb_core.notifier.Gotify`.
  - Configures union-returning route decorators with `response_model=None` to prevent Pydantic field serialization exceptions.
- **Typer CLI (`cli.py` & `__init__.py`)**: Exposes the console entrypoint `kb-web serve` to launch the Uvicorn host wrapper.
- **Template Migration (`templates/`)**: Moved all 7 Jinja2 HTML/text templates into the library package namespace.
- **Unit and Integration Tests (`tests/test_server.py`)**: Implemented a mock temp database context testing config fallbacks, Pydantic normalizations, public/private routes, and login validations.
- **Systemd Utility**:
  - **`kb-web.service`**: Systemd template for running the service as system user `will` under `/srv/kb-web` and loading environment secrets from a local `.env` file.
- **Project Documentation (`README.md` & `docs/`)**: Documented the project layouts, configurations, CLI commands, testing steps, and deployment variables in the local README and the mono-repo agent history.

---

## 2. Test Verification Output

All tests collected and executed inside the synchronized environment successfully passed:

```bash
$ uv run pytest
============================= test session starts =============================
platform win32 -- Python 3.13.13, pytest-9.0.3, pluggy-1.6.0
rootdir: remotes/kb-web
configfile: pyproject.toml
plugins: anyio-4.13.0
collected 5 items

tests\test_server.py .....                                               [100%]
======================== 5 passed, 1 warning in 1.24s =========================
```

---

## 3. Manual Verification & Setup Guide

### Local Verification
1. Run local dependencies synchronization:
   ```bash
   cd remotes/kb-web
   uv sync
   ```
2. Start the local server to verify execution:
   ```bash
   uv run kb-web serve --port 8050
   ```
3. Visit `http://localhost:8050/pages` to verify table loading. Enter valid credentials (default pass: `admin123` or override `KB_PASSWORD`) on `/` to trigger manual page ingests.

### Server Deployment Setup (Git Flow)
1. Git pull the repository on the server at `/srv/kb-web`.
2. Configure local file ownership:
   ```bash
   sudo chown -R will:will /srv/kb-web
   ```
3. Initialize Python venv and install the package:
   ```bash
   cd /srv/kb-web
   python3 -m venv .venv
   .venv/bin/pip install --upgrade pip
   .venv/bin/pip install .
   ```
4. Copy the service unit file to systemd and reload the daemon:
   ```bash
   sudo cp kb-web.service /etc/systemd/system/kb-web.service
   sudo systemctl daemon-reload
   sudo systemctl enable --now kb-web
   ```
