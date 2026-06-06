# KB Repo and KB Vault Package Creation

**Date**: June 5, 2026  
**Status**: Completed  

This document logs the porting and standalone package setup of `kb-repo` and `kb-vault` into the `remotes/` directory.

---

## 1. Packages Created

### `kb-repo` (Repository Scanner & Watcher)
- **Purpose**: Discovers and indexes local Git repositories on the host machine. Houses a background watcher daemon to update repository file records dynamically when changes occur on disk.
- **Commands**:
  - `kb-repo add <path>`: Register a directory to be scanned recursively for Git repositories.
  - `kb-repo remove <path>`: Deregister a directory from scanning.
  - `kb-repo list-paths`: View configured scan directories.
  - `kb-repo scan`: Traverses scan directories to locate repositories, indexes file metadata into `repo_files`, and indexes text contents matching target extensions into `repo_file_contents` (with FTS5).
  - `kb-repo list`: Show tracked repositories and count of indexed files.
  - `kb-repo watch start` / `stop` / `status` / `run`: Watcher daemon controls (uses `watchfiles` to perform high-performance directory polling).

### `kb-vault` (Obsidian Vault Scanner)
- **Purpose**: Discovers and indexes local Obsidian markdown vaults (directories containing a `.obsidian` folder).
- **Commands**:
  - `kb-vault add <path>`: Register a directory to scan.
  - `kb-vault remove <path>`: Deregister a directory from scanning.
  - `kb-vault list-paths`: View configured scan directories.
  - `kb-vault scan`: Recursively scans for Obsidian vaults and indexes markdown file metadata/contents.
  - `kb-vault list`: Show tracked vaults and count of indexed files.

---

## 2. Shared Database Integration

Both packages integrate directly with the user's local SQLite database located at `~/.kb/kb.db`.
- Schema definitions are applied on connection initialization dynamically to protect database safety.
- The `content_versions` table and triggers are registered automatically:
  - `copy_repo_file_to_versions_table_on_hash_change`
  - `copy_vault_file_to_versions_table_on_hash_change`
  - When file content changes, triggers automatically increment the file version and insert the historic record into the history log.

---

## 3. Configuration Management

Configurations are kept package-specific under:
- `~/.kb/configs/kb-repo.json`
- `~/.kb/configs/kb-vault.json`

If the package configuration is not found, both CLI commands automatically fall back to reading directories from the original `scan_config.json` located at `~/.kb/configs/scan_config.json`.
