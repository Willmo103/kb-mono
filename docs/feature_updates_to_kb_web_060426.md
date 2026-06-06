# Feature Updates to kb-web - June 4, 2026

## Overview
Added several major capabilities to the `kb-web` package:
- **Web Share Target login next redirection**: unauthorized users are redirected to login and immediately redirected back with all share parameters intact.
- **Quick Share browser bookmarklet**: drag-and-drop link on the import dashboard to easily share current browser links directly to kb-web.
- **Pasted URL extraction regex logic**: automatically parses the first URL from dirty copy-pasted text.
- **YouTube transcript fetching**: scrapes transcripts using `youtube-transcript-api` and page metadata via `yt-dlp` to index YouTube video contents.
- **Tags aggregator view**: renders a catalog of tags with counts and list filtered matching pages.
- **Semantic similarity comparison**: calculates description/tags vector embeddings using Ollama's embeddings API, storing them in the database, and listing semantically matching articles in page details.
- **Model Context Protocol (MCP) server**: runs a FastMCP stdio server enabling local agents to query, search, and list KB articles.

## Database Schema Modifications
- Added `article_embeddings` table (`url` PK, `embedding` TEXT JSON, `updated_at` TEXT) to store vector embeddings.

## CLI Subcommands
- Exposed `mcp` subcommand in typer cli to run FastMCP stdio server.

## Verification
- pytest unit tests coverage expanded to 100% passing (13 tests total).
- build pipeline executed successfully.
