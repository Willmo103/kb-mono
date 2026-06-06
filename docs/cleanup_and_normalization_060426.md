# KB Stack Cleanup and Normalization - June 4, 2026

## Overview
This document logs the changes and guidelines established during the cleanup and normalization loop of the `kb` application stack, focusing on packaging standalone Electron binaries, unified path staging, and CLI launcher integration.

---

## Technical Guidelines

### 1. Naming Conventions for Binaries
To prevent command collisions and execution conflicts in the user's system PATH between Python CLI wrappers and the Electron desktop GUIs:
- **Python CLI Wrapper**: Retains its standard package script name (e.g., `kb-clipboard`, `kb-rss`).
- **Electron GUI Standalone**: Copied to the staging path (`~/.kb/bin/`) and suffixed with `-desktop` (e.g., `kb-clipboard-desktop.exe`, `kb-rss-desktop.exe`).
- **Launcher CLI Commands**: The `serve` subcommand attempts to find the `-desktop` executable in the PATH and execute it directly.

### 2. Standalone DB Migrations and Seeding
Both Python background watcher services and Electron desktop applications must be capable of establishing and initializing the database independently:
- **Independent Connection Safety**: Before establishing SQLite connections, folders (`~/.kb` and `~/.kb/configs`) must be created dynamically if missing.
- **Auto-Schema Creation**: Table definitions and indexes (`CREATE TABLE IF NOT EXISTS...`) are run on connection initialization by both CLI and desktop main processes.
- **Auto-Seeding**: Default settings and data (e.g., `rss_feeds.json`) must be checked on initial run, and if the tables are empty, seeded locally without triggering external network requests.

---

## Build and Compilation Performance Metrics

Future agents compiling the Vite/React frontend assets and packaging them with `electron-builder` must be prepared for extended execution times, especially when files are copied over local network shares:

- **kb-clipboard Build Pipeline**: `~6 minutes and 15 seconds`
- **kb-rss Build Pipeline**: `~5 minutes and 50 seconds`

> [!TIP]
> **Timer Guidelines for Future Agents**
> When running the `build.py` script for these packages in the background, schedule a timer/cron reminder for `360 seconds` (6 minutes) before checking the logs for completion. Do not poll continuously, as it blocks execution.
