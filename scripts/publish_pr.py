# /// script
# requires-python = ">=3.13"
# dependencies = ["sqlite-utils", "typer", "rich"]
# ///
import sqlite_utils
from pathlib import Path
import subprocess
import typer
from rich.console import Console

app = typer.Typer(help="Commit changes, push, and mark draft PR as ready")
console = Console()

DB_PATH = Path(__file__).parent.parent / 'artifacts.db'
DB = sqlite_utils.Database(DB_PATH)

@app.command()
def publish_pr(
    repo: str = typer.Argument(..., help="The package name, e.g., kb-web"),
    changelog: str = typer.Argument(..., help="Changelog description to commit")
):
    """
    Commits any remaining modified files in the repository, pushes the branch,
    and marks the active draft Pull Request as ready for review on GitHub using 'gh'.
    """
    repo_path = Path(__file__).parent.parent / "remotes" / repo
    
    if not repo_path.exists() or not repo_path.is_dir():
        console.print(f"[bold red]Error:[/] Repository {repo} not found in remotes/")
        raise typer.Exit(code=1)

    # 1. Get current branch name
    try:
        branch_result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=repo_path, capture_output=True, text=True, check=True
        )
        current_branch = branch_result.stdout.strip()
    except subprocess.CalledProcessError as e:
        console.print("[bold red]Failed to detect current git branch.[/]")
        console.print(e.stderr)
        raise typer.Exit(code=1)

    if current_branch == "master":
        console.print("[bold red]Error:[/] You are on 'master' branch. You cannot publish master directly via this script.")
        raise typer.Exit(code=1)

    # 2. Stage and commit changes (if any modified files exist)
    status_result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repo_path, capture_output=True, text=True, check=True
    )
    
    if status_result.stdout.strip():
        console.print("[cyan]Staging and committing files...[/]")
        try:
            subprocess.run(["git", "add", "-A"], cwd=repo_path, check=True)
            subprocess.run(["git", "commit", "-m", f"Changelog: {changelog}"], cwd=repo_path, check=True)
        except subprocess.CalledProcessError as e:
            console.print("[bold red]Failed to commit modifications.[/]")
            raise typer.Exit(code=1)
    else:
        console.print("[yellow]No modifications detected to commit.[/]")

    # 3. Push to upstream
    console.print(f"[cyan]Pushing branch '{current_branch}' to origin...[/]")
    try:
        subprocess.run(["git", "push", "origin", current_branch], cwd=repo_path, check=True)
    except subprocess.CalledProcessError as e:
        console.print("[bold red]Failed to push changes to upstream.[/]")
        raise typer.Exit(code=1)

    # 4. Mark draft PR as ready
    console.print("[cyan]Marking draft Pull Request as ready...[/]")
    try:
        subprocess.run(["gh", "pr", "ready"], cwd=repo_path, check=True)
        console.print("[green]PR marked as ready for review.[/]")
    except subprocess.CalledProcessError as e:
        console.print("[bold red]Failed to mark PR as ready via gh CLI (it might already be ready).[/]")

    # 5. Update SQLite database to mark matching issues as resolved or PR published
    if 'issues' in DB.table_names():
        rows = DB.execute_returning_dicts(
            "select id from issues where repo = ? and branch_name = ?",
            [repo, current_branch]
        )
        for row in rows:
            try:
                DB["issues"].update(row["id"], {"status": "published"})
                console.print(f"[green]Logged status=published to issue ID {row['id']}[/]")
            except Exception as e:
                console.print(f"[bold red]Failed to update issue ID {row['id']} status:[/] {e}")

if __name__ == "__main__":
    app()
