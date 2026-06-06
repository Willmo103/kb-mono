---
name: create-python-github-workflow
description: Generates a standardized GitHub Actions workflow for testing, version-bumping, tagging, and creating GitHub Releases for Python libraries using uv.
---

# Create Python GitHub Workflow Skill

This skill provides step-by-step instructions and templates to generate a standardized, fully automated CI/CD workflow for Python libraries in their remote repositories.

---

## When to Use

Use this skill when you need to configure automated testing, version-bumping, tagging, and release creation for a Python library that uses the `uv` package manager.

---

## The Standard Workflow Template

A Python library workflow must be placed at `.github/workflows/test-and-release.yml` in the library's root directory. It must follow this exact template structure:

```yaml
name: Test and Release

on:
  push:
    branches:
      - master
      - main
  pull_request:

permissions:
  contents: write

jobs:
  test-and-release:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up uv
        uses: astral-sh/setup-uv@v5
        with:
          enable-cache: true

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"

      - name: Run tests
        run: |
          uv sync
          uv run pytest

      - name: Bump version and push release tag
        if: github.event_name == 'push' && (github.ref == 'refs/heads/master' || github.ref == 'refs/heads/main')
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          
          # Bump project patch version
          uv version --bump patch
          NEW_VERSION=$(uv version --short)
          
          # Stage and commit version changes
          git add pyproject.toml uv.lock
          git commit -m "chore: bump version to $NEW_VERSION [skip ci]"
          
          # Tag the release
          git tag "v$NEW_VERSION"
          
          # Push the commit and the tags back to the active branch
          BRANCH_NAME=${GITHUB_REF#refs/heads/}
          git push origin HEAD:$BRANCH_NAME --follow-tags
          
          # Create GitHub Release pointing to the new tag
          gh release create "v$NEW_VERSION" --title "Release v$NEW_VERSION" --notes "Automated release for version v$NEW_VERSION"
```

---

## Implementation Procedure

Follow these steps when implementing the workflow for a target Python library:

1. **Verify Prerequisites**:
   - Verify that the target library uses the `uv` build backend and package manager.
   - Verify that the library contains a `pyproject.toml` and a `tests/` directory with `pytest` configuration.

2. **Create Workflow File**:
   - Create a file at `<library_root>/.github/workflows/test-and-release.yml`.
   - Copy the template above into the file.
   - Adjust the target branch (e.g., `master` or `main`) to match the primary branch name of the repository.

3. **Verify the Configuration**:
   - Ensure the workflow has `permissions: contents: write` to allow committing, tagging, and creating GitHub Releases.
   - Ensure `GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}` is set in the release step environment to authorize the pre-installed `gh` CLI.
   - Ensure `fetch-depth: 0` is set in the checkout step to pull git history needed for tagging and pushing.

4. **Verify Locally**:
   - Ensure all tests run successfully locally with `uv run pytest` before committing/pushing the new CI workflow.
