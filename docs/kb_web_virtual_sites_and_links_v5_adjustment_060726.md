# KB Web Virtual Sites & Links Adjustment Log - June 7, 2026

## Overview
This log documents the second iteration of changes to `kb-web`, addressing user feedback on layout preferences and virtual sites.

---

## Technical Details

### 1. Site Wiki Removal
Removed site-wide wiki generation and cache table references from `server.py` and templates:
- De-registered and removed `/admin/regenerate/site-wiki` endpoint.
- Removed calls to `get_or_create_site_wiki` and the helper function definition.
- Modified `/view/site` route and template to display only the list of pages belonging to that site.

### 2. Page Header Re-layout
- Grouped the action buttons (Regenerate Wiki, Regenerate Tags, Re-fetch Page, Delete Entry, and Share Link) inside a vertical flex column aligned to the right of the title.
- Placed the yellow Tags badge section below this title/button flex container.

### 3. Sidebar Cleanup
- Removed tag display blocks from the similar articles listings inside the left sidebar on the page viewer layout.

---

## Verification
- Simplified the `test_virtual_sites` unit test in `tests/test_server.py` to match the adjusted sites design.
- Ran tests via `uv run pytest` and verified all 16 tests pass cleanly.
