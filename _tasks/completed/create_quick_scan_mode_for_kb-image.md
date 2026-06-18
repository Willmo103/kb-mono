# Task: Create Quick Scan (Metadata-Only) Mode and Back-filling for `kb-image`

## Problem Statement / Motivation
Currently, when importing a directory of images via `kb-image import --dir <path>`, the importer processes every single file by opening the image, extracting EXIF data, calculating the content hash, generating thumbnails, and base64-encoding the entire original image. 

Storing the full base64-encoded representation of every image inside the SQLite database immediately results in massive database bloat (e.g., 17GB for a single folder) and makes the import process extremely slow and resource-heavy.

We want a **Quick Scan (Metadata-Only) Mode** that indexes the metadata (path, name, size, timestamps, EXIF, dimensions, and hash) but leaves the heavy `image` and `thumbnail` fields empty. We also need a companion **Back-fill command** to load and store the full base64 images and thumbnails on demand (e.g., for specific images or in batches later).

---

## Technical Requirements

### 1. Model Updates (`src/kb_image/models.py`)
- Modify `BaseImage` to make `image` and `thumbnail` fields optional, since they will be empty during a metadata-only scan:
  - `thumbnail: Optional[str] = None`
  - `image: Optional[str] = None`

### 2. Importer Updates (`src/kb_image/process.py`)
- Update `process_file_image(file_path: Path, metadata_only: bool = False) -> Optional[ImageFile]`:
  - If `metadata_only` is `True`:
    - Open the image via PIL to extract EXIF and dimensions (very fast as it only reads the header, not the full pixel bytes).
    - Compute the SHA-256 `image_hash` of the file (required for primary key/deduplication).
    - Skip calling `generate_thumbnail` and `generate_base64_image`. Set `thumbnail = None` and `image = None`.
    - Return the `ImageFile` object with empty image/thumbnail fields.
- Update `import_image_files_from_directory`, `process_images_in_directory`, and `import_image_file` to accept and pass through a `metadata_only: bool = False` argument.

### 3. CLI Updates (`src/kb_image/cli.py`)

#### A. Import Subcommand Option
- Add a `--quick` / `-q` option (defaulting to `False`) to the `import` command:
  - Help text: `Import image metadata only, skipping base64 image and thumbnail generation.`
  - When `--quick` is specified, run the import process with `metadata_only=True`.

#### B. New `fill` Subcommand
Implement a new `fill` command to back-fill missing image data (full base64 and thumbnail) from disk:
```bash
kb-image fill [--all] [--limit <number>] [--hash <hash>] [--path <path>]
```
- **Arguments / Options**:
  - `--all`: Find all records in the database where `image` (or `thumbnail`) is `NULL` or empty, and back-fill them.
  - `--limit`: Limit the number of files to back-fill in this run (useful for batching).
  - `--hash`: Back-fill a specific image matching the content hash.
  - `--path`: Back-fill a specific image matching the file path.
- **Back-filling logic**:
  - Retrieve matching records from the database.
  - Verify if the file still exists at the recorded `path`. If not, log a warning and skip.
  - Process the file on disk to generate the base64-encoded image and thumbnail.
  - Update the database record using the primary key `image_hash`.

### 4. Verification & Testing
- Update `tests/test_image_logic.py` to add comprehensive test coverage:
  - Test importing an image with `metadata_only=True` and verify that the database record is created with `image = None` and `thumbnail = None`.
  - Test the back-filling command (`fill`) on an existing metadata-only record and verify that it successfully adds the thumbnail and base64-encoded image.
  - Test that missing files on disk during back-filling are handled gracefully without crashing the CLI.
