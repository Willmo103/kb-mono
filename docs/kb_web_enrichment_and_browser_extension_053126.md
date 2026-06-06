# Feature Update - kb-web Enrichment, Settings Portal & Browser Extension
**Date:** May 31, 2026  
**Agent ID:** Antigravity

This document logs the feature additions to `remotes/kb-web` extending the web ingestion target server with administrative configuration inputs, metadata tagging, AI curation triggers, and a Manifest V3 browser extension for manual page submission.

---

## 1. Overview of New Features

- **Web Admin Settings Form**: Prefills and saves Ollama hosts/models, custom wiki system prompts, Chrome API keys, and Gotify targets. Saves changes to the config file `~/.kb/configs/kb-web.json` without requiring system reboots.
- **Wiki Title extraction**: The wiki cleanup prompt has been updated to enforce generating a markdown H1 title (`# Title`) at the start of the wiki entry. The server automatically parses this line and writes it to the database `title` column.
- **Tag Curation and Manual Editing**:
  - Automatically queries Ollama to categorise pages with 5-10 tags during ingestion.
  - Displays tags as color-coded labels in the UI.
  - Allows manual tag overrides via an inline editor panel.
- **AI Re-generation Triggers**: Adds **Regenerate Wiki** and **Regenerate Tags** controls on the profile viewer page, prompting Ollama to re-process content in real-time.
- **Administrative Access Controls & Deletion**:
  - Gated all interactive actions (regenerate wiki, regenerate tags, manual tag editing, and page deletion) behind `is_admin` security checks on the user interface.
  - Added an administrative `POST /admin/delete/page` endpoint to permanently delete pages from the database.
- **Browser Extension Target Endpoint**: Exposes a secure POST route `/api/import/html` which requires header authentication (`X-API-Key`) matching the server config.
- **Chrome Browser Extension**: An unpackaged Manifest V3 extension under `browser_extension/` that retrieves the active tab HTML and URL, posts it to the FastAPI API, and displays badge notifications: "SYNC" (blue), "OK" (green), "ERR" (red) with reset timers.
- **GitHub Actions CI/CD Workflow**: Implemented a workflow at `.github/workflows/test-and-release.yml` that runs pytest and automatically bumps the patch version, tags the commit, and pushes it back to master upon pushes, without creating a GitHub release.

---

## 2. Database Schema Updates

The SQLite database table `fetched_pages` was updated to incorporate two new columns:
- `title` (text): Used to catalog article headers.
- `tags` (text): Stores JSON-encoded arrays of keywords/labels.

To ensure older database instances do not break, the database connection manager automatically runs a migration routine:
```python
columns = db["fetched_pages"].columns_dict
if "title" not in columns:
    db["fetched_pages"].add_column("title", str)
if "tags" not in columns:
    db["fetched_pages"].add_column("tags", str)
```
This migration is safe and preserves all historical records.

---

## 3. UI Modifications

- **pages_list.j2.html**: Cards now display the parsed page `title` in bold as the main header, showing the raw URL as smaller text underneath.
  - Displays "+ Ingest New Target" linking to `/import` only if authenticated.
- **view_page.j2.html**: Renders tag badges, adds controls for manual tag overrides, triggers real-time Ollama regeneration, and implements options menus. All edit/update actions and the new **Delete Entry** button are wrapped inside `{% if is_admin %}` blocks so they are hidden from regular viewers.
  - Added warning banner when reading historical versions, with a version switcher to view snapshots.
  - Added **Re-fetch Page** button to the administrator controls.
- **admin.j2.html**: Exposes the full configuration form allowing updates to system parameters, API key passcodes, Gotify credentials, and system prompts.
  - Added **Change Admin Password** form panel.
- **base.j2.html**: Refactored top header navigation bar to dynamically render access points ("🔑 Admin Login" when unauthenticated; "+ Ingest URL", "Admin Dashboard", and "Logout" when authenticated).

---

## 4. Verification & Testing

Unit tests were added in `tests/test_server.py` to assert API key authentication checks, configuration persistence loops, Pydantic tag arrays, route parameters, admin-only UI restrictions, administrative page deletions, logout mechanisms, secure password updates, and versioned page re-fetching.
All tests completed successfully:
```
tests\test_server.py .........                                           [100%]
======================== 9 passed, 1 warning in 2.08s =========================
```
