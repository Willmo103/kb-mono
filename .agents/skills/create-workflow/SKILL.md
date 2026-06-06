---
name: create-workflow
description: Guides the agent through the process of planning, structuring, formatting, and implementing new automated workflows in the `.agents/workflows/` directory.
---
# Create Workflow Skill

This skill provides instructions and standards for designing and implementing agent workflows within the mono-repo. Workflows are automated, step-by-step procedures executed by agents when triggered by slash commands in the chat interface.

---

## 1. Directory Structure and Command Mapping

Workflows are defined as markdown files inside the `.agents/workflows/` directory. The filename directly maps to the slash command exposed in the user interface.

- **Location**: `c:\Users\Will\Desktop\will_mono\.agents\workflows/`
- **Naming Convention**: Lowercase, hyphen-separated, ending with `.md` (e.g., `update-documentation.md`).
- **Trigger**: The slash command is the filename without the `.md` extension (e.g., `/update-documentation`).

---

## 2. File Format and Structure

Every workflow file must adhere to the following template structure:

```markdown
---
description: <A clear, 1-sentence description of the workflow's purpose. This description appears next to the slash command in the UI.>
---

# <Workflow Title>

## Context
<Explain why this workflow is needed, who uses it, and the high-level goals or constraints.>

## Setup
<List any prerequisites, environment variables, or setup scripts that must run before the process begins (e.g., scripts/setup_commit_workflow.py). Define placeholder variables like $commit_id or $run_id.>

## Process
<Numbered list of sequential steps to guide the agent during execution. Each step must define a clear task, specific tool commands to run, and the expected inputs/outputs.>

## Success Criteria
<List concrete conditions that verify the workflow has been completed successfully.>

## Abort/Error Handling
<Define how the agent should handle failure, rollback changes, or clean up temporary files in case of interruption.>
```

---

## 3. Workflow Standards & Best Practices

To maintain a consistent development cycle and support auditing, all workflows must implement the following standards:

### 3.1 Setup Scripts & Run-Specific Artifacts
Every workflow that executes automated scripts or modifies code MUST:
1. Include a companion python setup script (e.g., `scripts/setup_*_workflow.py`).
2. Run the setup script in the **Setup** phase to generate a unique run ID and create a dedicated artifact output folder (e.g., `artifacts/<type>/$run_id/`).
3. Store all logs, diff files, and intermediate results of the run inside that run-specific directory.

### 3.2 Development Artifact Versioning
When creating design/plan files during a development loop, the agent must save them under `artifacts/development/<some_name>/<date>_<change_desc>/` in the workspace.
- **Strict Version History**: Do not overwrite plan files when making modifications based on user review/comments. Instead, save subsequent iterations sequentially (e.g., `plan_1.md`, `plan_2.md`, `plan_3.md`).
- **Standard Outputs**: Ensure the development directory also contains `tasks.md` (to track progress) and `walkthrough.md` (upon completion).

### 3.3 Resiliency and Cleanup
Workflows must include explicit rollback instructions to leave the repository in a clean state in the event of failure or aborting.

---

## 4. Decision Logic for Workflow Types

When designing a new workflow, you must decide how it will manage its artifacts and state tracking. Use the following decision matrix:

| Criterion | Script-Driven (Owned Artifacts) | Centralized / Data-Driven |
| --- | --- | --- |
| **Typical Use Case** | Discrete development loops (e.g., imports, commits, remote updates). | Ongoing tracking, quick status checks, or ad-hoc tasks (e.g., todos). |
| **Artifact Directory** | A unique folder created for each run: `artifacts/<type>/$run_id/` | None. Reads/writes directly to a root-level index or database. |
| **Execution ID** | Unique ID generated dynamically by a setup script (e.g., `$commit_id`). | Persistent or database-level record IDs (e.g., 8-character task UUIDs). |
| **Ownership** | The workflow "owns" the directory and generates multiple discrete tracking files (e.g., `plan.md`, `git_diff.md`). | The workflow interacts with a shared registry; the user or other scripts drive updates. |
| **Template Reference** | [owned_artifact_workflow_template.md](file:///c:/Users/Will/Desktop/will_mono/.agents/skills/create-workflow/templates/owned_artifact_workflow_template.md) | [centralized_data_workflow_template.md](file:///c:/Users/Will/Desktop/will_mono/.agents/skills/create-workflow/templates/centralized_data_workflow_template.md) |

### Choosing the Workflow Archetype

1. **Category A: Script-Driven (Owned Artifacts)**
   - *Choose this if* the task requires a defined "before" and "after" state, multiple discrete files of logs/diffs/plans specific to that run, and needs to be isolated from other runs.
   - *Example*: Release commits and package imports. A setup script creates the directory, and the workflow populates it with a `plan.md`, `git_diff.md`, and `affected_packages.md`.

2. **Category B: Centralized / Data-Driven (User or Utility Driven)**
   - *Choose this if* the task is an ongoing, cumulative registry where multiple agent runs or user requests append data to the same place, and the data does not belong to a specific development loop.
   - *Example*: The Todo system. It uses `_todos` to store all active items across the entire monorepo, updated interactively, without creating execution directories.

---

## 5. Workflow Creation Process

To create a new workflow:

1. **Identify the Need**: Clarify what repetitive developer tasks or agent loops need automation.
2. **Draft the Frontmatter**: Write a concise, user-facing description for the YAML frontmatter.
3. **Draft the Process Steps**: Outline the setup, sequence of actions, and success/abort criteria.
4. **Create the File**: Save the markdown file in `c:\Users\Will\Desktop\will_mono\.agents\workflows/<command-name>.md`.
5. **Update Repository Documentation**: Record the newly created workflow in the repository documentation index if required by the standards.
