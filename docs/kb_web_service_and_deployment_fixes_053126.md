# Feature Update - kb-web Service & Deployment Fixes
**Date:** May 31, 2026  
**Agent ID:** Antigravity

This document logs the troubleshooting and fixes applied to the systemd service and script configurations to ensure successful deployment on Linux production servers.

---

## 1. Overview of Deployment Issues & Solutions

1. **Systemd Environment File Constraint**:
   - **Problem**: Systemd would fail with `Failed to load environment files: No such file or directory` if the configuration file `.env` was missing or not yet generated at the target location `/srv/kb-web/.env`.
   - **Solution**: Added the `-` prefix to the `EnvironmentFile` directive in `kb-web.service` (`EnvironmentFile=-/srv/kb-web/.env`) to make loading the file optional during startup.

2. **Systemd Executable Constraint**:
   - **Problem**: Executing standard `uv run kb-web` inside the unit `ExecStart` fails because systemd expects absolute paths and does not inherit terminal python binary PATHs.
   - **Solution**: Configured `ExecStart` to directly target the compiled virtualenv binary: `/srv/kb-web/.venv/bin/kb-web --host 0.0.0.0 --port 8050`.

3. **Virtual Environment Setup Failures**:
   - **Problem**: The recommended setup process in `README.md` (`python3 -m venv .venv` and `pip install .`) failed on the server because standard `pip` cannot resolve the `kb-core` git dependency mapped in the UV-specific `tool.uv.sources` table.
   - **Solution**: 
     - Replaced standard pip commands in `README.md` with `uv sync` to ensure correct Git dependency resolution and virtual environment creation.
     - Updated `scripts/install_service.sh` to dynamically resolve the parent path to `kb-web.service` relative to the script directory.
     - Enhanced the script to check for `/srv/kb-web/.venv/bin/kb-web` and automatically execute `uv sync` to scaffold the environment if it is missing and `uv` is present on the server.

4. **Automated Build Pipeline**:
   - **Solution**: Created `build.py` at the root of `remotes/kb-web` to orchestrate synchronization (`uv sync`), test execution (`uv run pytest`), and package compilation (`uv build`), aligning `kb-web` with the repository standard.

---

## 2. Verification

The updated automated build pipeline and test suite were run successfully, compiling packaging artifacts:
```
=========================================
Step: Synchronizing environment & dependencies
Running: uv sync
=========================================
Resolved 51 packages in 1ms
Audited 51 packages in 5ms

=========================================
Step: Running pytest suite
Running: uv run pytest
=========================================
tests\test_server.py .........                                           [100%]
======================== 9 passed, 5 warnings in 3.33s ========================

=========================================
Step: Building source and wheel packages
Running: uv build
=========================================
Successfully built dist\kb_web-0.1.5.tar.gz
Successfully built dist\kb_web-0.1.5-py3-none-any.whl

[SUCCESS] Build pipeline completed successfully!
```
