# Design Plan 1: kb-web Feature Enhancements (v6)

Detailed design is document in implementation_plan.md.
Summarized features:
1. Cosine similarity threshold >= 0.8 in `get_similar_articles`.
2. Segment YouTube videos into their own section on the website, filter by creator, display iframe in view page, and write specialized LLM prompt for video breakdowns.
3. Preprocess wiki markdown to fix singular asterisks lists and missing blank lines.
4. Expose SSE transport for FastMCP in `cli.py` and provide `kb-web-mcp.service`.
5. YouTube metadata is saved in a separate `youtube_videos` table to decouple from standard pages schema.
