# /// script
# requires-python = ">=3.13"
# dependencies = ["sqlite-utils", "typer", "rich"]
# ///
import sqlite_utils
from pathlib import Path
import subprocess
import typer
from rich.console import Console
from rich.panel import Panel
import sys


def get_uv_cmd() -> str:
    import shutil

    uv_path = shutil.which("uv")
    if uv_path:
        return uv_path

    local_bin = Path.home() / ".local" / "bin"
    candidate = local_bin / ("uv.exe" if sys.platform == "win32" else "uv")
    if candidate.exists():
        return str(candidate)

    return "uv"


app = typer.Typer(help="Run pre-commit checks on a package submodule")
console = Console()

DB_PATH = Path(__file__).parent.parent / "artifacts.db"
DB = sqlite_utils.Database(DB_PATH)


@app.command()
def check(repo: str = typer.Argument(..., help="The package name, e.g., kb-web")):
    """
    Validates package status before a commit: checks for CHANGELOG updates,
    runs code formatting/lint checks, and runs pytest if test folder exists.
    """
    repo_path = Path(__file__).parent.parent / "remotes" / repo

    if not repo_path.exists() or not repo_path.is_dir():
        console.print(f"[bold red]Error:[/] Repository {repo} not found in remotes/")
        raise typer.Exit(code=1)

    all_passed = True
    console.print(Panel(f"Running Pre-Commit Checks for: {repo}", style="bold magenta"))

    # 1. Check if CHANGELOG.md is modified
    console.print("[cyan]Checking for CHANGELOG.md modification...[/]")
    try:
        # Check diff including unstaged and staged files
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True,
        )
        status_output = result.stdout.strip()
        has_changelog = "CHANGELOG.md" in status_output

        # Also check git diff of unstaged/staged to see if it's there
        if has_changelog:
            console.print("[green]✔ CHANGELOG.md is modified/staged.[/]")
        else:
            # Maybe it is already committed in the current branch but not on master?
            # Let's check files changed in branch compared to master
            branch_res = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=True,
            )
            current_branch = branch_res.stdout.strip()
            if current_branch != "master":
                diff_files_res = subprocess.run(
                    ["git", "diff", "--name-only", "master...HEAD"],
                    cwd=repo_path,
                    capture_output=True,
                    text=True,
                    check=True,
                )
                if "CHANGELOG.md" in diff_files_res.stdout:
                    has_changelog = True
                    console.print(
                        "[green]✔ CHANGELOG.md modification detected in branch commits.[/]"
                    )

            if not has_changelog:
                console.print(
                    "[yellow]⚠ WARNING: CHANGELOG.md is not modified or staging is clean. Please ensure you update CHANGELOG.md.[/]"
                )
                all_passed = False
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error running git status check:[/] {e.stderr}")
        all_passed = False

    # 2. Run Ruff lint/format check if ruff is available
    console.print("\n[cyan]Checking code style and formatting (Ruff)...[/]")
    uv_cmd = get_uv_cmd()
    try:
        # Check if ruff is runnable in uv context or system
        linter_res = subprocess.run(
            [uv_cmd, "run", "ruff", "check", "."],
            cwd=repo_path,
            capture_output=True,
            text=True,
        )
        if linter_res.returncode == 0:
            console.print("[green]✔ Code styling checks passed (Ruff check).[/]")
        else:
            console.print("[red]❌ Code style check failed (Ruff check issues):[/]")
            console.print(linter_res.stdout or linter_res.stderr)
            all_passed = False
    except FileNotFoundError:
        # Fallback to system ruff
        try:
            linter_res = subprocess.run(
                ["ruff", "check", "."], cwd=repo_path, capture_output=True, text=True
            )
            if linter_res.returncode == 0:
                console.print(
                    "[green]✔ Code styling checks passed (system Ruff check).[/]"
                )
            else:
                console.print(
                    "[red]❌ Code style check failed (system Ruff check issues):[/]"
                )
                console.print(linter_res.stdout or linter_res.stderr)
                all_passed = False
        except FileNotFoundError:
            console.print(
                "[yellow]⚠ Ruff is not installed/runnable. Skipping lint check.[/]"
            )

    # 3. Run Pytest if test directory exists
    test_dir = repo_path / "tests"
    if test_dir.exists() and test_dir.is_dir():
        console.print("\n[cyan]Running unit tests (Pytest)...[/]")
        try:
            test_res = subprocess.run(
                [uv_cmd, "run", "pytest"], cwd=repo_path, capture_output=True, text=True
            )
            if test_res.returncode == 0:
                console.print("[green]✔ All tests passed successfully.[/]")
            else:
                console.print("[red]❌ Unit tests failed (Pytest):[/]")
                console.print(test_res.stdout or test_res.stderr)
                all_passed = False
        except FileNotFoundError:
            try:
                test_res = subprocess.run(
                    ["pytest"], cwd=repo_path, capture_output=True, text=True
                )
                if test_res.returncode == 0:
                    console.print("[green]✔ All tests passed successfully.[/]")
                else:
                    console.print("[red]❌ Unit tests failed (Pytest):[/]")
                    console.print(test_res.stdout or test_res.stderr)
                    all_passed = False
            except FileNotFoundError:
                console.print(
                    "[yellow]⚠ pytest is not installed/runnable. Skipping test execution.[/]"
                )
    else:
        console.print("\n[yellow]No tests/ folder found. Skipping tests.[/]")

    console.print("\n" + "=" * 40)
    if all_passed:
        console.print("[bold green]✔ PRE-COMMIT CHECKS PASSED SUCCESSFULLY![/]")
    else:
        console.print(
            "[bold red]❌ PRE-COMMIT CHECKS FAILED. Please resolve the warnings/errors above.[/]"
        )
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
