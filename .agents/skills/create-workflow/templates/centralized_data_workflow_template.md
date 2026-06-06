---
description: Template for a data-driven workflow that interacts with centralized data stores or registries without run-specific directories.
---

# Centralized Data Workflow Template

## Context
This template is for workflows that represent interactive or ongoing tasks (e.g., managing tasks, updating status indices, or checking services). These workflows write to or read from a shared centralized index or database.

## Setup
1. Ensure the central data store or file (e.g., `_todos` or local database) is present. If not, initialize it using the setup script:
   ```shell
   python scripts/setup_<data_store>_artifact.py
   ```

## Process
1. **Interactive Query/Creation**: Prompt the user or inspect files to gather inputs.
2. **Database Update**: Use the helper scripts to modify the central store (e.g., adding, updating, or deleting entries):
   ```shell
   python scripts/create_<item>.py
   ```
3. **Index Refresh**: Re-generate any formatting or tables to display the updated state to the user:
   ```shell
   python scripts/get_<items>.py
   ```

## Success Criteria
- The centralized data store is successfully updated.
- The new/updated entry is printed to stdout or visible in the central file.

## Abort/Error Handling
In case of database lock or write error:
- Catch exceptions and report them clearly to the user.
- Avoid corrupting the central index by performing atomic or validated writes.
