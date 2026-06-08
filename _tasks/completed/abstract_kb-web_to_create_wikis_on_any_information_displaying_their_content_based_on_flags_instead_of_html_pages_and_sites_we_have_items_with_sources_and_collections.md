# Task: Abstract `kb-web` to Create Wikis on Any Information

## Motivation / Problem Statement
Currently, `kb-web` is designed specifically to ingest and display web pages (`fetched_pages` table) and group them by domain name to generate website profiles (`site_wikis` table). This tightly binds the application to HTML documents and web URLs.

However, the user wants `kb-web` to serve as a generalized knowledge portal for the entire `kb` stack—including image metadata (`kb-image`), clipboard clips (`kb-clipboard`), Obsidian vault notes (`kb-vault`), and RSS articles (`kb-rss`).

We need to abstract the `kb-web` architecture. Instead of hardcoded HTML web pages and domain sites, the application will model all data as **Items** belonging to **Sources** and **Collections**, using dynamic **Flags** (e.g., tags, categories, read/unread status, archives) for categorization and filtering. The wiki generation system should be abstracted to summarize and create wiki profiles for *any* source or collection.

---

## Technical Requirements

### 1. Data Schema Abstraction (`src/kb_web/db.py` & `src/kb_web/models.py`)
Replace the specific `fetched_pages` and `site_wikis` database schema with generalized models:

- **`items` Table**:
  - `id`: Primary key (UUID or content hash).
  - `title`: Title of the item.
  - `content`: Primary text/markdown body.
  - `content_type`: Categorization identifier (e.g., `web_page`, `youtube_video`, `image`, `text_clip`, `obsidian_note`).
  - `source_id`: ForeignKey linking to the `sources` table.
  - `metadata`: JSON string holding content-type-specific values (e.g., EXIF for images, original URL/HTML headers, links list, file paths).
  - `tags`: JSON string array of tags.
  - `flags`: JSON string array of boolean flags/states (e.g., `["favorite", "unread", "archived", "needs_wiki"]`).
  - `created_at` & `updated_at`: Timestamps.

- **`sources` Table**:
  - Represents the origin of items (e.g., `github.com` for web, `clipboard` for clips, `/users/will/vault` for Obsidian).
  - `id`: Primary key (unique slug/path).
  - `name`: Display name.
  - `type`: Type of source (e.g., `web_domain`, `local_directory`, `system_daemon`, `rss_feed`).
  - `wiki_content`: Cached LLM-generated summary/wiki profile for this source.
  - `updated_at`: Timestamp.

- **`collections` Table**:
  - Logical groups of items defined by users or automated curation agents.
  - `id`: Primary key (slug).
  - `name`: Display name.
  - `description`: Textual summary.
  - `wiki_content`: Cached LLM-generated summary/wiki profile for this collection.
  - `updated_at`: Timestamp.

- **`item_collections` Table**:
  - Junction table for many-to-many relationship between `items` and `collections`:
    - `item_id`: ForeignKey referencing `items.id`.
    - `collection_id`: ForeignKey referencing `collections.id`.
    - PK: `(item_id, collection_id)`.

- **Migration Script**:
  - Write a migration routine in `db.py` to port existing `fetched_pages` and `site_wikis` data into `items`, `sources`, and `collections` without losing data.

### 2. Generalizing the Wiki Generator (`src/kb_web/server.py`)
- Refactor the wiki generation logic:
  - Implement a generic `get_or_create_wiki(entity_type: str, entity_id: str)` supporting both `"source"` and `"collection"`.
  - For a selected source or collection, query all associated items.
  - Concatenate item descriptions and details, and prompt Ollama to generate a synthesized markdown wiki profiling the source/collection.
  - Cache the result in the corresponding `sources` or `collections` table.

### 3. Dynamic UI Driven by Flags, Collections, and Sources
- **Sidebar Navigation**:
  - Replace hardcoded "Articles" and "Sites" views with a dynamic sidebar navigation:
    - **Flags Segment**: Quick filters based on item flags (e.g. "Favorites", "Unread", "Archived").
    - **Collections Segment**: Lists all records in the `collections` table.
    - **Sources Segment**: Lists all records in the `sources` table.
  - Selecting any flag, collection, or source updates the dashboard center panel to list the matching items.
- **Item Detail View**:
  - Display item details based on its `content_type`.
  - Add an interactive tag editor and a dynamic checklist of **Flags** to toggle attributes on/off (e.g. toggling `favorite` or `archived` states).
  - Embed wiki sections for the item's source and collections directly on the page, with buttons to regenerate them.

### 4. Verification & Testing
- Update and refactor unit tests in `tests/test_server.py`:
  - Write tests for the migration script to verify data integrity.
  - Test creating items, assigning them to sources/collections, and verifying flag-based filtering queries.
  - Test generating wiki profiles for sources and collections.
