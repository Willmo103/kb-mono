# Qdrant and EmbeddingGemma Integration

This document outlines the design decisions and research regarding the integration of **EmbeddingGemma** (Google's Gemma-based embedding model) and **Qdrant** for vector storage and retrieval.

---

## 1. EmbeddingGemma Prefix Guidelines

Research indicates that **EmbeddingGemma** is an instruction-tuned embedding model trained to excel at asymmetric search (retrieval-augmented generation, or RAG) and symmetric search (clustering, similarity). 

To achieve optimal retrieval performance, EmbeddingGemma requires task-specific instruction prefixes:
- **For Documents/Passages (Storage)**: Prepend `"search_document: "` to the text chunk before embedding.
- **For Queries (Retrieval/Search)**: Prepend `"search_query: "` to the user's query text before embedding.

### Example Usage with Ollama API:
```python
# Embedding a document chunk
response = client.embeddings(
    model="embeddinggemma",
    prompt="search_document: " + chunk_content
)
vector = response["embedding"]  # 768-dimensional float array
```

Using the correct prefix ensures the model projects queries and passages into the correct semantic subspace, leading to significantly higher recall and precision.

---

## 2. Qdrant Storage and Schema Design

Qdrant is configured to store points in the **default vector space** (i.e. unnamed single vectors) matching the length of `embeddinggemma` (768 dimensions) with **Cosine** distance.

### REST Payload Structure for Collection Creation:
```http
PUT /collections/{{collection_name}}
Content-Type: application/json

{
  "vectors": {
    "size": 768,
    "distance": "Cosine"
  }
}
```

### REST Payload Structure for Point Upsert:
```http
PUT /collections/{{collection_name}}/points
Content-Type: application/json

{
  "points": [
    {
      "id": "{{point_uuid}}",
      "vector": [0.012, -0.045, ...],
      "payload": {
        "source_type": "articles",
        "source_id": "https://example.com/article",
        "source_title": "Example Article Title",
        "chunk_number": 0,
        "chunk_content": "The actual text of the chunk...",
        "created_at": "2026-06-16T12:00:00Z",
        "item_note": "Markdown notes added by user/agent...",
        "taxonomy_path": "/Folder/Subfolder/Item.md"
      }
    }
  ]
}
```

---

## 3. Determinstic UUID Generation for Points
To prevent duplicate records in Qdrant when re-syncing or re-exporting the same collection, point IDs are generated deterministically as Version 5 UUIDs using the URL namespace combined with a unique string representation of the source and chunk index:
```python
import uuid
point_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{source_type}:{source_id}:{chunk_number}"))
```
This ensures that if the same chunk is exported multiple times, it receives the exact same UUID in Qdrant, overwriting/updating the existing vector and payload.

---

## 4. Future MCP Integration Outlook
The Qdrant collection database will expose endpoints that allow external Model Context Protocol (MCP) servers to:
1. Receive search queries from agents.
2. Embed the search queries with Ollama using the `"search_query: "` prefix.
3. Query Qdrant using similarity matching.
4. Inject context-rich document chunks directly into agent conversations.
