---
description: Template for a script-driven workflow that owns and creates discrete run-specific artifacts.
---

# Script-Driven Artifact Workflow Template

## Context
This template is for workflows that represent discrete development loops (e.g., code imports, package creations, or repository releases). It generates a unique directory and files for each run to track plans and git diffs.

## Setup
1. Run the setup script to generate a new run ID and initialize the artifact directory:
   ```shell
   python scripts/setup_<workflow_name>_workflow.py
   ```
   *Note: Use the generated `$run_id` and directory path in the following steps.*

## Process
1. **Planning**: Use workspace analysis tools to inspect the target code or environment. Create the planning document at `artifacts/<workflow_name>/$run_id/plan.md`.
2. **Execution**: Execute the changes step-by-step as outlined in the planning document.
3. **Verification**: Run tests or compiler commands to verify correctness.
4. **Logging**: Generate the final execution report at `artifacts/<workflow_name>/$run_id/execution_report.md`.

## Success Criteria
- The planning document is completed and approved by the user.
- The step-by-step changes pass all verification checks.
- The execution report is generated in the run-specific directory.

## Abort/Error Handling
In the event of failure:
- Clean up any half-written files in the run directory.
- Revert changed files using `git restore`.
- Report the failure reasons to the user.
