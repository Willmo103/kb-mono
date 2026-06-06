# kb-clipboard Overview

`kb-clipboard` is a system clipboard manager and history manager designed for the `kb` ecosystem. It tracks system copy events, stores clipboard history in SQLite, and provides an Electron-based React desktop browser interface for searching and recovering past clipboard items.

## Package Structure

The repository is organized into a Python backend service package and an Electron React GUI frontend:

- **[src/kb_clipboard/watcher.py](../remotes/kb-clipboard/src/kb_clipboard/watcher.py)**: The clipboard watcher daemon. Checks the clipboard periodically (default 0.2s) for changes:
  - Supports text, file paths, and images.
  - Generates EXIF data and JPEG thumbnails for images.
  - Automatically deduplicates entries via SHA-256 hashes.
  - Automatically truncates history to a maximum of 500 rows.
  - Avoids double-capture of CLI actions using `clip_skip.txt`.
- **[src/kb_clipboard/cli.py](../remotes/kb-clipboard/src/kb_clipboard/cli.py)**: Command-line interface exposing:
  - `watch`: Runs clipboard watcher in foreground.
  - `start` / `stop` / `status`: Launches or stops background daemon silently (via `pythonw`).
  - `serve`: Launches Electron React application (automatically updates/downloads executable if not found).
  - `install`: Database migrations, registers background autostart triggers on logon, builds system PATH bindings, and configures Desktop shortcuts.
  - `update`: Queries GitHub release channel and downloads the latest prebuilt Electron executable.
  - `import-json`: Imports legacy JSON clipboard backups.
- **[desktop/](../remotes/kb-clipboard/desktop)**: Electron React desktop application.
  - `main.js`: Intercepts minimize/close events to collapse window into the system tray, queries SQLite database directly using `sqlite3` driver, and bridges native copy actions.
  - `src/`: React GUI matching Earth-toned retro aesthetics (`solarized-light`).

## Build & CI/CD Pipeline

- **[build.py](../remotes/kb-clipboard/build.py)**: Python build script compiling frontend UI assets, packaging Electron app, running pytest suites, and building Python wheel packages.
- **[.github/workflows/test-and-release.yml](../remotes/kb-clipboard/.github/workflows/test-and-release.yml)**: GitHub Actions workflow that executes tests on pull requests and automates version bumps, compilation, and uploading prebuilt Windows binaries onto GitHub releases on merge to master/main.
