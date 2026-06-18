# Update `kb-web` iteration 8

**ALL CHANGES TO THE `kb-web` REPO MUST BE RAN ON A SEPERATE BRANCH WHICH MUST BE CREATED BY THE AGENT AT THE INITIALIZATION OF THE PLAN** the branch will be named `feature-enhanced-collections` and will be a branch of the current `kb-web` local master branch HEAD.

Below are the required changes to the codebase **kb-web** ordered from low to high complexity (according to the user):

## Fixing Issues:

1. When moving from admin panel (after viewing logs) I get a 500 error for every link I click on. The 500 page displays and says it has been logged to the admin panel (but it was also supposted to gotify message me the stacktrace for all errors).

This is the error message recieved when this happens. Sometimes when the server ingests something large (possibly using multiple AI calls to the server since a transcript is too large) this starts to happen, and I have to restart the service on the server.

```shell
[2026-06-16 05:13:57,324] ERROR in server: Uncaught exception: disk I/O error
Traceback (most recent call last):
  File "/srv/kb-web/.venv/lib/python3.13/site-packages/starlette/middleware/errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "/srv/kb-web/.venv/lib/python3.13/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "/srv/kb-web/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "/srv/kb-web/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/srv/kb-web/.venv/lib/python3.13/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "/srv/kb-web/.venv/lib/python3.13/site-packages/starlette/routing.py", line 660, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/srv/kb-web/.venv/lib/python3.13/site-packages/starlette/routing.py", line 680, in app
    await route.handle(scope, receive, send)
  File "/srv/kb-web/.venv/lib/python3.13/site-packages/starlette/routing.py", line 276, in handle
    await self.app(scope, receive, send)
  File "/srv/kb-web/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 134, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "/srv/kb-web/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "/srv/kb-web/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/srv/kb-web/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 120, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "/srv/kb-web/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 674, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
    )
    ^
  File "/srv/kb-web/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 330, in run_endpoint_function
    return await run_in_threadpool(dependant.call, **values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/srv/kb-web/.venv/lib/python3.13/site-packages/starlette/concurrency.py", line 32, in run_in_threadpool
    return await anyio.to_thread.run_sync(func)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/srv/kb-web/.venv/lib/python3.13/site-packages/anyio/to_thread.py", line 63, in run_sync
    return await get_async_backend().run_sync_in_worker_thread(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        func, args, abandon_on_cancel=abandon_on_cancel, limiter=limiter
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/srv/kb-web/.venv/lib/python3.13/site-packages/anyio/_backends/_asyncio.py", line 2518, in run_sync_in_worker_thread
    return await future
           ^^^^^^^^^^^^
  File "/srv/kb-web/.venv/lib/python3.13/site-packages/anyio/_backends/_asyncio.py", line 1002, in run
    result = context.run(func, *args)
  File "/srv/kb-web/src/kb_web/routers/pages.py", line 39, in view_all_pages
    db = _get_db()
  File "/srv/kb-web/src/kb_web/base.py", line 41, in _get_db
    init_db(db)
    ~~~~~~~^^^^
  File "/srv/kb-web/src/kb_web/db.py", line 38, in init_db
    if "fetched_pages" not in db.table_names():
                              ~~~~~~~~~~~~~~^^
  File "/srv/kb-web/.venv/lib/python3.13/site-packages/sqlite_utils/db.py", line 636, in table_names
    return [r[0] for r in self.execute(sql).fetchall()]
                          ~~~~~~~~~~~~^^^^^
  File "/srv/kb-web/.venv/lib/python3.13/site-packages/sqlite_utils/db.py", line 542, in execute
    return self.conn.execute(sql)
           ~~~~~~~~~~~~~~~~~^^^^^
sqlite3.OperationalError: disk I/O error

```

2. (possibly related to above) Ingestion Timeout -- When the server is processing a large import (e.g. a youtube transcript that takes multiple calls to the Ollama API), the server times out giving a CloudFlare 524 timeout error. I know that the process completed because I get the gotify notification to my phone. -- I think that we just need to yeild and display progres on the webpage from the call to the API.

3. The backup JSON nolonger provides a true backup or sync, since the JSON does not include all of the information like embeddings, transcripts, or chunking information, etc. We need to update the backup JSON to include all of the information from the database **AFTER** all of the changes (and subsequent changes) -- This should be added as a rule in the appropriate GEMINI files in kb-web and kb-mono. **NOTE**: This also means that the import process should likely be updated to allow the full database backup to be applied via JSON.

4. The display of the key icons for `Page Entry` and `Tag Title` on the similarity graph page do not show their icons (attached image)

## Modifications

### General

1. I want remove the `play` button from the video list entries; instead making the image the link to open the entry page; the play button is misleading. (attached image)

2. I want to likewise have the article `Open Entry` button to be removed and instead have the row be a clickable link to open the entry page. (this can be in a lower Z-index than the current clickable links, I just dont like having to aim for that tiny button, or how it looks on the page). (attached image)

### Logging Changes (Admin Panel)

- I want to have a longer cache of current log entries, essentially set a limit for logs of 10k lines and allow the user to select how many lines of previous logs to view up to 10k (default should be 1k)
- I want to be able to download the current logs selected in the view in a txt format

### Collections changes

**User's Roadmap Objective -- a high-level overview of the end-goal/use-case scenario.**
>
> The main idea here is to start fleshing out the way that I am going to start relating all of the types of information that I am importing; from the clipboard history to the rss feeds I am liking and commenting on, to the obsidian vaults, and repos scattered across my computer, My whole goal here has been, in short, to 'help remember where the fuck I put that thing, where I heard that at, where I learned to do that thing, what I was even doing?'. Partially to track my actions and save information into a central place, but I want to move into creating curated information collections that can be related to everything but also viewed in their narrow scope. Right now kb-web has morphed into the central hub of my information gathering (with kb-rss and the extension pointing to the application now) I plan on moving the kb-vault and kb-repo logic into the kb-web application *in a way* in a future expansion, but what I mean by that is that I will soon be importing notes, batches of code, and other files like PDFs, audio, and images. and using some of the structrure of the kb stack in the web application. The **MAIN GOAL** for this iteration of the process is going to be to inbitialize the collection database code and the API connection to the qdrant server code so that in the future everything may be built off of that without needing to refactor the core collection code. this is the main **pipeline** for the future of the kb stack. We must be able to handle high volumes of import data for all types of user input. This is also the main driver ofkb-web's continued existence.
>

We are going to advance the collections aspect of the kb-web in order to allow the user to generate both general and collection-specific vector-embeddings from the main content, the summaries, then we will use the tags as sparce vectors to help make up for lack of information in the dense vector embeddings when considering an entry against a query from a different collection or context.

- We will need to update the database to incorperate the chunking and embedding of the main content, attaching some metadata to the chunk table entry (like documnet_id, chunk_idx, document_source_url, etc. This should be the dynamic information *accompanying* the embedding vector.) This should be formatted to be used in `Qdrant`. **This should not be a breaking issue when the vector store is unreacheable, and should NOT be tested before pushing to prduction. This feature will be tested in a developemnt environment pointing to a production qdrand server, this should be treated as a migration and not a kb-web dependency**. The goal is to *sync* the vectors and metadata to a dqrant cluster to be used for vector store stuff, but kb-web will always be the source of truth.

#### Vector Generation/Regeneration

We will need to generate embeddings for all of the current un-embedded pages in the database, and in this case we are not using the descriptions (alone) we are going to create new embedding tables **specifically for use with qdrant* that will embed the descriptions, and the full md-content in a cleaned fashion using the google embedding model `embeddinggemma` which has specific prefixes that can be used for specific embedding *document* types or querries. (This should be researched by the agent for this task and documented in an artifact with the sources found/used for this). This will also be focused on the useage of qdrant for querying by the user and agents via a future MCP addition, keeping that in mind the usage of `qrdant` should also be researched by the agent and stored in the artifact docs for kb-web and the use of `embeddinggemma` for embedding purposes should also be researched by the agent and documented in the same artifact. These critical features are hilighy important for the next phase of kb-web development.

**New Concepts**

 - *Collection Item* -- The abstract table that will represent items in a collection. The prime relation is to collection and the source should be stored as source_table source_id This table will house the following conceptual information and will represent information as it relates to the collection processes.
  - *Collection Item Notes* -- Each item in a collection is a frozen object, imutable but there should be a markdown note attached to the item that can be used as the 'obsidian' style note for the user or the agent to edit and annotate the item.
   - the notes will be columns that are attached to the collection and associated to the parent article/video/code/image/etc. using a simple text field and not an actual relationship field. (to allow for a abstract association)
   - Colection Item Notes are Markdown formatted.
   - Note Frontmatter fields for these notes may be used to inform agent interactions and future agent driven organization of items. **This is just an idea, but it seems like a good way to add context to documents**
  - *Collection Item Taxonomy Path* -- A virtual, agent driven, view layer for a collection wherin the items are 'organized' into a filetree style taxonomy with the associated note being the `document` view layer for the immutable collection item.
  - *Collection Visibility* -- A collection may either be `public` or `private`. Public collections are visible to non admin users, private collections are only visible to the admin user.
 - *Collection Actions* -- Collection action are any actions that are non-trivial. these actions serve as the collection manager agent menory. e.g. the agent is asked to create a short entry for the addition to the collection every time an item is added to the collection as a b/g process.
 - *Collection Editor* -- The file-tree obsidian md-note editor/viewer populated with the collection_item source info and wiki entry on a view pannel and the empty collection_item.item_note content as a empty markdown note where they may edit it (there would also be a chat pannel for chatting with the agent. that agent would be able to edit that file, create a new collection item based on the user's input etc.)
  - Items may be imported directly into a collection through the collection editor (essentially using whatever import path that it naturally would, and adding the collection_item id to the collection xref table associating it with the specific collection table entry.)
  - Notes **Not** associated to a specific collection_item may be created in a collection these should be stored elsewhere in the database associated to the collection, Possibly on disk. They should however be a part of the collection context for exports and imports as well as for the agent. An agent may create non-item notes as well. These should be mutable and deletable by the user, and mutable by the agent; deletable via permissioned request
  - The User shoud be able to create skills and workflows for the collection via the editor and test them out with the agents. (this could be like how to create a specific report using information in the colleciont or using a specific script or template)
 - *General Collection* -- The general_collection is the collection that every item will become a part of by default. It will essentially be the default collection view for every item.
  - Admin's can specify items that should be excluded from the general collection; marking them `private` or `public` via a check-box on the article/video [code/note/etc.] page, or in the multi-select list view of either videos or articles [ or any other type of media that will be introduced in the future].
  - On migration the admin user will have to trigger a process where the each item will be added to the general_collection table as a collection_item this is primarially to generate the collection_items rows, but also to allow the agent to populat the taxonomy of the general collection. As this is populated we would start to see the notes available in the collection editor


The following code processes will need to be created:

- A process to initialize the new collection system:
 1. Migratte the database tables to support the new collection system (migrating the current collection contents, but leaving the taxonomy empty for the agent to fill in after filling in the general collection as it is being initialized. )
 2. Create a process in the admin portal to populate the **genreal** collection (the specific collections will be handles in the specific collection page):
  - This process passes each article/video with its collection metadata to the agent, the agent uses a tool call to pass its parameters (we just read them, no need to use a function call just have the tool return the arguments, we will just grab the args from the call anyways and never actually call the tool) <taxonomical/path/in/general/collection> <collection_action_note> We will have it pass the relitive path in the "root folder" of the collection (the relitive path from the root folder of the collection, not the absolute path on the disk) and the collection action note to the agent. We check those arguments and store them in the database. (The path doesn't need to be checked, since its just a virtual representation of the taxonomical importance of the information related to everything else.)
  - We just keep doing this, re-trying on errors, and processing items until all have been processed. (Ie. create the collection_item, then the colection note, etc.)
  - create embeddings for all items:
   - Creates an agnostic embeddings table for each type of content (article_embeddings, video_embeddings, etc. [in the future we will have a table `repo_file_embeddings` and `note_file_embeddings` for the repo and vault files])
   - SET A MAX_CHUNK_LEN of 1500 characters for embedding chunking process (HARDCODED for embeddinggemma) NO CHANGES
   - SET a CHUNK_OVERLAP of 150 characters (HARDCODED for embeddinggemma) NO CHANGES
   - parse and chunk each item's md_content (or main content field for other future classes)
    - embed with embeddinggemma via Ollama using the appropriate prefixes to attach any semantic metadata to the vector. (whatever the embeddinggemma docs suggests for this sort of storage/retreival) store the resulting chunk into the database.
   - parse the item's description field and embed it into the database as well. [same process as above]
   - populate the chunk_metadata feilds appropriatly for qdrant and store the information in the chunk. Chunk_metadata should be as follow:
    - `source_type` (articles, videos)
    - `source_id` (the id of the article or video)
    - `source_title` (the title of the article or video)
    - `chunk_number` (the chunk number of the article or video)
    - `chunk_content` (the content of the chunk)
    - `chunk_vector` (the embeddings of the chunk)
    - `created_at` (the date and time the chunk was created)

3. Create a process where a specific collection may be exported to the qdrant server via API

This process should gather all of the collection_items and their associated data, chunk_metadata, vectors, and collection_item_notes from the database, and then package it in such a way that it can be imported into the qdrant server and use the configured `QDRANT_HOST_URL` and `QDRANT_API_KEY` to configure a client and upload the points to the server ( if the server is offline the points are stored locally and synced when the server comes back online).
- The format should be such that the points are stored in a collection named `collection_name` (the name of the collection). This will allow the user to have multiple collections in the qdrant server, each in its own collection.
- The points should be stored in the "default" collection space, not a named collection
- This process should first check if the collection already exists in the qdrant server, and if it does, it should sync the points to the server points taking the local changes over the server's. (This will require us to keep track of the version/signature of a collection, which should be updated every time the collection is exported.)

#### Collections Page Changes

- *I want to be able to add entries to a collection without having to be on that entry's page (e.g. from the collections page)*
- *I don't want changes to take place until I click a `save changes` button when I have multiple items selected* (this also applies when I am removing items, reordering items, etc.)
- I want to be able to select multiple entries to add to a specific collection on the collection page.
- I want to be able to remove multiple entries from a collection in the collection view.
- I want to be able to assign items to multiple collections (this should be a given seeing that the general_collection will already have everything in it)
- I want to be able to drag and drop items in the collection view to reorder them. (dragging an item into a collection div, then having that item shown in the list of items as a different color until the changes are saved)

#### Collections Agent (LLM Changes to Collection suggestion)

The collection suggestion process and buttons should be removed since the agent will be managing the collections by default. The admin will still be able to manually add items to the collection, but the agent will be responsible for populating the taxonomy of the general collection as well as the specific collections, and will be able to create notes in collections, re-order and re-renk collection items in whichever collection they are opperating in.

each collection should expose its agentic setting on the collection page if you are admin. the agent settings should include the system prompts used for the RAG sub-agent for the collection, the taxonomy agent for the collection and some sort of general system context object like a JSON or something that can house global variables or context that the agent can access or will be provided in each agent turn (stuff like {{datetime}}, {{workspace.foldername.filename.extension}}, {{taxonomy_tree_str}} etc.) these are just examples, but I want the option to pass variables to prompts that relate to specific things in the collection (or on the server as a workspace) and context to or from the agent (and it should persist for the duration of the session/turn)


