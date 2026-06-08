# kb-image Overview

`kb-image` is the image-explorer and tagger component of the `kb` ("Knowledge-Base") ecosystem. It manages scanning local directories or downloading web links, indexing image files, extracting EXIF metadata, creating thumbnails, classifying image categories, generating AI-based descriptions (using Ollama), and viewing assets in a native desktop Electron application.

## Module Structure

The package is structured as a standalone python package with the following modules inside `src/kb_image/`:

- **[config.py](../remotes/kb-image/src/kb_image/config.py)**: Configures default values such as `MIN_FILE_SIZE` (10KB), `SUPPORTED_EXTENSIONS` (`.jpg`, `.jpeg`, `.png`, `.webp`), and initializes the Ollama client (defaulting to the remote address `http://192.168.0.25:11414`).
- **[models.py](../remotes/kb-image/src/kb_image/models.py)**: Pydantic-based data models. Defines `BaseImage` (core metadata including dimensions, created/modified times, classifications, and tag lists) and `ImageFile` / `WebImage` (extending the base model with specific source paths or origin URLs).
- **[utils.py](../remotes/kb-image/src/kb_image/utils.py)**: Image processing helpers, including PIL image validations (`validate_and_get_image_info` checking minimum size and valid format) and base64 encoders (`get_base64_image_file`).
- **[process.py](../remotes/kb-image/src/kb_image/process.py)**: Orchestrates importing tasks. Handles downloading web URLs, running classification/description, converting full-resolution images and thumbnails into SQLite BLOBs/base64 strings, and executing database insertion.
- **[image_classification.py](../remotes/kb-image/src/kb_image/image_classification.py)**: Categorizes images into groups (`nature`, `people`, `screenshots`, `diagrams`, `memes`, `other`).
- **[image_describer.py](../remotes/kb-image/src/kb_image/image_describer.py)**: Connects to Ollama (via LLAVA/multimodal LLMs) to generate detailed, contextual descriptions of imported images.
- **[image_tagger.py](../remotes/kb-image/src/kb_image/image_tagger.py)**: Processes descriptions to automatically generate tags for uncategorized images using Ollama chat prompts.
- **[cli.py](../remotes/kb-image/src/kb_image/cli.py)**: Main entry point for the `kb-image` command-line utility. Defines commands:
  - `import`: Imports a single file (`-f`), directory (`-d`), or url (`-u`). Supports the `--quick` / `-q` flag to import metadata-only without generating base64 images and thumbnails.
  - `serve`: Launches the compiled Electron desktop application.
  - `tag`: Automatically loops through untagged database rows and generates tags.
  - `fill`: Back-fills missing base64 original images and thumbnails from disk. Supports `--all`, `--limit <limit>`, `--hash <hash>`, and `--path <path>` to target records.

## Desktop User Interface

The React frontend under desktop/ is packaged into a native desktop Electron application that connects directly to the SQLite database `~/.kb/kb.db` (bypassing any HTTP API server):

- **[main.js](../remotes/kb-image/desktop/main.js)**: Configures window preferences, reads/writes SQLite database tables using the Node `sqlite3` driver, and handles web image imports by spawning the python subprocess `uv run kb-image import --url <url>`.
- **[preload.js](../remotes/kb-image/desktop/preload.js)**: Exposes secure IPC endpoints to the React renderer window via `contextBridge`.
- **[App.jsx](../remotes/kb-image/desktop/src/App.jsx)**: Renders a solarized-light/retro-dark styled layout with infinite scrolling thumbnails, metadata drawer, EXIF tag explorer, and tag manager.

## Build & Testing

The package includes:
- **[build.py](../remotes/kb-image/build.py)**: Pipeline script that compiles Vite frontend assets, compiles the native sqlite3 electron bindings, packages the portable Electron standalone app to `desktop/dist/`, synchronizes python packages, runs pytest unit tests, and builds python distributions.
- **tests/**: Complete test suite for all modules inside the repository.
