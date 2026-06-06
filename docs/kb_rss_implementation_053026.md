# kb-rss Curation App Implementation - May 30, 2026

I have implemented the complete `kb-rss` feed reader and AI curation tool under `remotes/kb-rss` using a Python background watcher, CLI, and Electron React desktop client. This document outlines the technical design, the offline scraping reader view, the webview implementation, and CLI error handling updates.

## 1. Technical Components & Schema

- **Database integration**: Configured `kb-rss` to read and write directly to `~/.kb/kb.db` (initialized using `sqlite-utils` and shared with `kb-core`).
- **Offline Scraper**: Integrated `BeautifulSoup` to parse external web articles on-demand via `fetch-full <entry_id>` command, stripping script/nav/header blocks and converting relative image links to absolute URLs.
- **Embedded browser tag & Dynamic HTML Export**: Integrated Electron's guest `<webview>` browser tag (enabling `webviewTag: true` in `BrowserWindow` webPreferences) to display websites. Added a `dom-ready` hook in React that automatically executes `document.documentElement.outerHTML` inside the webview and calls a new `save-raw-html` IPC handler to cache the raw page HTML offline.
- **Safe Sandboxed Iframe**: Updated the Summary Reader view to detect if the cached content is raw HTML (starting with doctype or containing html tags). If raw HTML is found, it renders it safely offline inside an `iframe` using `srcDoc` and `sandbox="allow-same-origin"`, keeping the core application styles and scripts isolated.
- **Windows PID Status Resolution**: Solved the Windows status check bug across both `kb-rss` and `kb-clipboard`. Since calling `os.kill(pid, 0)` raises `ValueError` on Windows, updated `is_pid_running` to query active process handles natively using `ctypes.windll.kernel32.OpenProcess`.
- **AI Agentic Curation**: Triggered via `agent-run` CLI subcommand. Uses local Ollama server (running `gemma4`) to update tastes, analyze latest entries, curate digests, and post summaries to Gotify.

## 2. Key Resolutions & Error Handling

- **Renderer ReferenceError**: Solved the `ReferenceError: shell is not defined` crash in Vite compiled assets. Because the frontend code runs in isolated browser context, it must not access Node/Electron `shell` or `clipboard` modules directly. Replaced with context-bridged `window.api.openUrl` IPC handlers.
- **CLI Exception Propagation**: Refactored `agent.py` to raise exceptions (rather than swallowing them and returning empty strings) and updated `cli.py` to exit with a non-zero code (`1`) on failure, ensuring that connection errors (like Ollama offline or bad hosts) are correctly reported back to Electron.
- **Dynamic Schema Migration**: Added checks in database initializers to dynamically append the `full_content` column to existing `rss_feed_entries` tables, preventing schema crashes on systems where the database was pre-existing.
