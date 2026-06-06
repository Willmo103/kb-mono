# kb-core Overview

`kb-core` is the foundational library for the `kb` ("Knowledge-Base") ecosystem of applications. It provides central configuration management, notification integration, template rendering, and standard utility functions.

## Module Structure

The package is structured as a standalone python package with the following modules:

- **[config.py](../remotes/kb-core/src/kb_core/config.py)**: Central configuration. Defines `Config` representing directory roots (defaulting to `~/.kb`), helper method `get_db()` (returns a `sqlite_utils` database connection), and `get_config_file()` to fetch config files under the `configs/` directory.
- **[notifier.py](../remotes/kb-core/src/kb_core/notifier.py)**: Notifier client integrating with Gotify. Includes standard hooks to send app messages (POST) and fetch message logs (GET) using `httpx`.
- **[renderer.py](../remotes/kb-core/src/kb_core/renderer.py)**: Jinja2-based HTML renderer. Defines `Renderer` to autoescape and compile HTML templates, rendering them either to string or directly to a static directory.
- **[types.py](../remotes/kb-core/src/kb_core/types.py)**: Declares core repository structures and root directory entity types via the `RootTypes` class (e.g., `IMAGE`, `VAULT`, `REPO`, `CLONED`, `DOCUMENT`).
- **[skip_dirs.py](../remotes/kb-core/src/kb_core/skip_dirs.py) / [skip_exts.py](../remotes/kb-core/src/kb_core/skip_exts.py) / [target_exts.py](../remotes/kb-core/src/kb_core/target_exts.py)**: Central lists containing directory exclusions, ignored extensions, and valid embeddable target file extensions.
- **[utils.py](../remotes/kb-core/src/kb_core/utils.py)**: Contains standard package utility functions including:
  - File embed validation (`is_embeddable_file`)
  - File text safe reader (`read_file_text`)
  - File size conversion (`human_size`)
  - Unique ID and hashing helpers (`get_uuid`, `hash_content`, `generate_image_hash`)
  - Ignoring directories/files checklist (`should_ignore_path`)
  - CLI folder trees renderer (`build_tree_string`)
  - Pillow image helper functions (`generate_thumbnail`, `extract_exif`)
  - GitHub Release asset download and check helpers (`download_github_release_asset`, `check_github_latest_release`)

## Build & Testing

The package includes:
- **[build.py](../remotes/kb-core/build.py)**: Script at the root to sync dependencies (`uv sync`), run tests (`pytest`), and build distribution packages (`uv build`).
- **tests/**: Complete test suite for all modules inside the repository.

*Note: For detailed code signatures, inspect the individual source files.*
