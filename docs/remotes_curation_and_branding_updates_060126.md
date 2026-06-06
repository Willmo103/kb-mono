# Remotes Curation & Branding Updates - June 01, 2026

## Objective
Standardize user branding, enable detached background processes for Electron apps, and introduce cross-application page scraping ingestion.

## Key Changes

### 1. Retro National Park Icons & Tray Setup
- Created flat PNG/SVG custom icons for `kb-clipboard`, `kb-rss`, `kb-image`, and `kb-web`.
- Generated multi-res `.ico` Windows builder assets and 16x16px task tray/favicon files.
- Embedded branded logos inside README files.

### 2. Detached CLI Launch
- Refactored server commands inside `cli.py` across `kb-clipboard`, `kb-rss`, and `kb-image` to run background GUIs via `subprocess.Popen` with Windows creation flags `0x00000008 | 0x08000000` (DETACHED_PROCESS | CREATE_NO_WINDOW), immediately returning control to the terminal.

### 3. Curation Feed & Backend Improvements (`kb-rss`)
- Implemented `published_today` bit flag in SQLite DB.
- Added background timestamp parsing to `watcher.py` loop.
- Sorted curation grids by `rowid DESC`.
- Added collapsible sidebar menu and split-view layout for **RSS Sources** in `App.jsx`.
- Constrained Ollama curation query to current-day articles.

### 4. Ingestion Web Interface (`kb-web`)
- Added `/api/import/page` POST endpoint to parse `HTMLPage` JSON payloads from external scrape clients.
- Implemented `/admin/test-gotify` and `/admin/test-ollama` connection testing helper routes.
- Added AJAX-driven test buttons to settings form.
- Mounted `/favicon.ico` route.
- Added search query input and tag list display on index template.

### 5. Scraper Integration & Curation Fallback
- Integrated `html2text` in `kb-rss` to convert raw webpage HTML to markdown files.
- Configured scraper in `kb-rss` to POST full structures to `kb-web` API for automatic summary generation.
- Implemented fallback logic in `kb-rss/agent.py` to automatically fall back to recent uncurated feed entries if no new feeds were published on the current calendar day, preventing empty agent runs.

### 6. kb-web Integration Settings & Manual Import
- Integrated configuration properties `kb_web_url` and `kb_web_api_key` in `kb-rss` python backend config, Electron `main.js` settings loaders, and React `App.jsx` settings tab.
- Added a manual "Import to kb-web" action button in `kb-rss` details drawer, which scrapes/uploads the page by executing the newly added `import-to-web` CLI command in `kb-rss/cli.py`.

### 7. Gunicorn Production Server Runner
- Created a standard programmatic `gunicorn_runner.py` inside `kb-web` that programmatically configures and runs Gunicorn with `UvicornWorker` on POSIX/Linux platforms, falling back gracefully to Uvicorn on Windows.
- Integrated the runner into `kb-web serve` CLI command.

