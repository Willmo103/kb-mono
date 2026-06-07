# KB Web Virtual Sites & Links Integration Log - June 6, 2026

## Overview
This development loop addresses requirements specified in the `v5` update task for the `kb-web` application. The changes implement virtual sites domain-grouping, an interactive link-ingestion workflow with confirmation modals, sidebar reorganizations, and collapsible markdown views.

---

## Technical Details

### 1. Database Schema
Created the `site_wikis` table to cache generated site-wide wiki profiles and prevent duplicate LLM calls:
```python
db["site_wikis"].create(
    {
        "site": str,
        "wiki_content": str,
        "updated_at": str,
    },
    pk="site",
)
```

### 2. URL Basename Extraction
Implemented the `get_url_basename` helper to standardize and group URLs under their root domains (stripping subdomains like `www.`):
- `https://github.com/trending` -> `github.com`
- `https://github.com/foo/bar` -> `github.com`

### 3. Site-Wide Wiki Synthesizer
Added `get_or_create_site_wiki` which retrieves individual page descriptions belonging to a specific domain, combines them, and prompts Ollama to write a cohesive, comprehensive summary of the site as markdown. The generated summaries are cached in `site_wikis`.

### 4. Interactive Links List & Modal Ingestion
On the `/view/page` route:
- Filtered scraped hyperlinks to only display links sharing the same root domain.
- Filtered out heading/fragment-only links (e.g. `href="#header"`).
- Implemented a modal popup confirmation UI. Clicking an un-ingested link opens the modal. Confirming submits a POST request to `/import/url` to trigger the ingestion pipeline.

### 5. Layout Adjustments
- Moved the "Semantically Similar Articles" panel to a sticky left sidebar on the page view.
- Added a left sidebar for the site profile view to browse other domains.
- Rendered original page markdown content as HTML inside a collapsible details section instead of printing raw markdown text.

---

## Verification
- Added `test_virtual_sites` unit test to `tests/test_server.py` exercising domain grouping, profile views, site-wiki generation, and admin regeneration.
- Ran test suite using `uv run pytest` and verified all 16 tests pass cleanly.
