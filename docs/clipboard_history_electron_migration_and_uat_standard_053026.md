# Clipboard History Migration & Electron App UAT Standard - May 30, 2026

I have implemented the migration of the `clipboard-history` PyQt6 application into an Electron + Python CLI application under `remotes/kb-clipboard`. I have also established the User Acceptance Testing (UAT) process standard for developing Electron applications.

## 1. Electron App UAT Standard

When developing Electron desktop applications in this repository, the agent must adhere to the following UAT standard:

- **Local Setup & Frontend Compile**: The agent must install local Node.js dependencies (`npm install`) and build the frontend bundle (`npm run build`) to ensure the application is functional in both production and development modes.
- **Interim UAT Block**: The agent **MUST** perform User Acceptance Testing (UAT) with the user before executing the final `build.py` script (which generates binary packages). This allows the user to run the application in their local environment, explore the interface, and report back any feedback or issues.
- **Feedback Loop**: Only after receiving the user's explicit UAT feedback and confirmation should the agent run the final build packaging and finalize documentation.

This process has been documented in the repository documentation and is established as a standard for all future Electron projects.

## 2. Clipboard History Migration Implementation

- **Python Daemon (Watcher)**: Replaced PyQt6 with a lightweight Windows API listener (`pywin32` + `Pillow`) in `watcher.py` to poll the clipboard every 200ms. It stores text, files, and base64-encoded screenshots/thumbnails into `kb-core`'s database at `~/.kb/kb.db`.
- **Skip Self-Copy**: Implemented a file-based lock mechanism (`~/.kb/clip_skip.txt`) where the Electron UI writes the hash of copied content to skip double-logging.
- **Typer CLI**: Added `cli.py` exposing CLI commands:
  - `watch`: Starts the clipboard watcher synchronously in the foreground.
  - `start`: detached process background launch (using `subprocess` creation flags on Windows), writing PID to `~/.kb/clipboard_watcher.pid`.
  - `stop`: terminating the PID securely.
  - `status`: checking process status.
  - `serve`: launching the Electron application.
- **Electron Client**: Direct SQLite queries (`sqlite3` Node bindings), a system tray icon showing 5 most recent clipboard items, window auto-hide on blur (focus loss), and a beautiful earth-toned React/Tailwind frontend styled exactly like `kb-image`.
