# Walkthrough - `kb-web` Settings, Curation & Chrome Extension Updates

I have successfully implemented all features approved in the design plan inside `remotes/kb-web`. The package now supports full configuration management via the admin UI, automatically parses titles and generates tag lists via Ollama, offers 1-click real-time re-generation triggers, and includes an unpackaged Manifest V3 Chrome extension.

---

## 1. Feature Implementations

### A. Configurations Management
- **config.py**: Added settings properties: `ollama_model` (default `gemma4:latest`), `api_key` (default `kb-secret-key`), and `wiki_prompt` system prompt, along with Gotify attributes. Developed a `save()` method that persists settings in `~/.kb/configs/kb-web.json`.
- **admin.j2.html**: Form inputs allow editing all settings (hosts, models, extension keys, Gotify endpoints/tokens, system prompts) and posts them directly to `/admin/config`.

### B. Title & Tag Curation
- **Database Schema Auto-Migration**: When starting up, `db.py` automatically checks for `title` and `tags` columns on the `fetched_pages` table and runs SQL schema updates to append them if they are missing, ensuring backward compatibility.
- **Title Extraction**: Modified the system prompt to require that generated wiki summaries begin with H1 headers (`# Title`). The FastAPI server automatically parses this line and writes it to the database `title` column.
- **Tag Generation & Manual Override**: 
  - Added an Ollama classification prompt that returns comma-separated tags for incoming pages.
  - Renders tag pills inside the page viewer UI.
  - Exposes an inline tag editor form allowing manual overrides.

### C. Real-Time Regenerators
- **view_page.j2.html**: Integrated **Regenerate Wiki** and **Regenerate Tags** button triggers. Clicking them triggers a POST to the server, runs the latest prompt/model in Ollama, updates the database row, and reloads the view page.

### D. Chrome Extension Module (`browser_extension/`)
- **API Endpoint**: Exposes a secure POST endpoint `/api/import/html` that processes raw HTML submissions. Requires header verification matching the configured settings `X-API-Key`.
- **Extension Scripting**: 
  - **manifest.json**: Declares Manifest V3 parameters with limited permissions (`activeTab`, `scripting`, `storage`).
  - **background.js**: Listens to toolbar icon clicks. Uses `chrome.scripting.executeScript` to extract DOM HTML, retrieves options settings, and posts payloads to the API. Displays visual icon badge indicators: "SYNC" (blue), "OK" (green), "ERR" (red) with clean reset timeouts.
  - **options.html & options.js**: Settings page styled in a premium solarized cream theme allowing users to input API target endpoints and tokens.

### E. Administrative Protection & Page Deletion
- **Admin-Only UI Gates**: Wrapped all interactive actions (Regenerate Wiki, Regenerate Tags, manual Edit Tags trigger, and the delete form) inside `{% if is_admin %}` blocks in `view_page.j2.html`. This ensures that regular viewers cannot access or view these mutation controls.
- **Administrative Delete Route**: Added a new route `POST /admin/delete/page` to `server.py`, protected by session auth guards (`verify_auth`). Clicking the **Delete Entry** button prompts the administrator with a confirmation dialog, deletes the entry from the sqlite database, and redirects them to the pages catalog.

### F. CI/CD Workflow Setup
- **GitHub Actions Workflow File**: Created a new workflow file at [test-and-release.yml](../remotes/kb-web/.github/workflows/test-and-release.yml).
- **Behavior**:
  - Automatically runs pytest suite on every push and pull request.
  - On push to the main `master` branch, it uses `uv version --bump patch` to increment the library's patch version.
  - Commits the updated version details back to the active branch (using `[skip ci]` to prevent recursive triggering) and tags it with the new version (e.g. `v0.1.x`).
  - Pushes the version bump commit and version tag back to origin.
  - It intentionally does *not* trigger a GitHub Release, as requested.

---

## 2. Test Verification Output

All tests in `tests/test_server.py` passed successfully (7 passed, verifying the new admin/deletion rules):

```bash
$ uv run pytest
============================= test session starts =============================
platform win32 -- Python 3.13.13, pytest-9.0.3, pluggy-1.6.0
rootdir: remotes/kb-web
configfile: pyproject.toml
plugins: anyio-4.13.0
collected 7 items

tests\test_server.py .......                                             [100%]
======================== 7 passed, 1 warning in 2.05s =========================
```

---

## 3. Manual UAT Instructions

### Chrome Extension Setup
1. Open `chrome://extensions/` in Chrome and enable **Developer mode**.
2. Click **Load unpacked** and select the folder `/srv/kb-web/browser_extension`.
3. Open the options page of the extension. Set endpoint: `http://localhost:8050/api/import/html` and API Key: `kb-secret-key` (or matching your configuration).
4. Go to any website and click the toolbar action icon. Check that the badge flashes "SYNC" then green "OK", and the page is imported into `http://localhost:8050/pages`.

### Configurations, Deletion & Tag Updates
1. Visit the Admin portal at `http://localhost:8050/admin`. Verify that Ollama host/model, prompts, and Gotify targets prefill correctly, and that clicking **Save Configurations** successfully persists updates.
2. Open any article page as a regular viewer (unauthenticated/logged out). Verify that the buttons for "Regenerate Wiki", "Regenerate Tags", "Delete Entry", and "Edit Tags" are completely hidden from the user interface.
3. Authenticate/Log in, then navigate back to the article page. Verify that all admin controls ("Regenerate Wiki", "Regenerate Tags", "Delete Entry", "Edit Tags") are fully visible.
4. Click **Delete Entry**, confirm the popup prompt, and check that the entry is permanently removed from the database and you are redirected to `/pages`.
