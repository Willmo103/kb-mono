# /// script
# requires-python = ">=3.13"
# dependencies = ["sqlite-utils", "typer", "rich"]
# ///
import sqlite_utils
from pathlib import Path
import subprocess
import typer
from rich.console import Console

app = typer.Typer(help="Create a new git branch and draft PR for issues")
console = Console()

DB_PATH = Path(__file__).parent.parent / 'artifacts.db'
DB = sqlite_utils.Database(DB_PATH)

@app.command()
def draft_pr(
    repo: str = typer.Argument(..., help="The package name, e.g., kb-web"),
    branch_name: str = typer.Argument(..., help="Name of the branch to create"),
    issue_ids: str = typer.Argument(..., help="Comma-separated list of issue IDs in artifacts.db (e.g., 1,2)")
):
    """
    Creates a new branch in the target sub-repository, makes an empty initial commit,
    pushes it to origin, creates a draft PR on GitHub via the 'gh' CLI, and logs the PR URL to artifacts.db.
    """
    repo_path = Path(__file__).parent.parent / "remotes" / repo
    
    if not repo_path.exists() or not repo_path.is_dir():
        console.print(f"[bold red]Error:[/] Repository {repo} not found in remotes/")
        raise typer.Exit(code=1)

    # Convert issue IDs to integers
    try:
        ids = [int(i.strip()) for i in issue_ids.split(",") if i.strip()]
    except ValueError:
        console.print("[bold red]Error:[/] Issue IDs must be comma-separated integers.")
        raise typer.Exit(code=1)

    # Verify 'gh' CLI is installed
    try:
        subprocess.run(["gh", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        console.print("[bold red]Error:[/] The GitHub CLI ('gh') is not installed or not in PATH.")
        raise typer.Exit(code=1)

    # 1. Checkout master and pull latest
    console.print(f"[cyan]Syncing {repo} with master...[/]")
    try:
        subprocess.run(["git", "checkout", "master"], cwd=repo_path, check=True, capture_output=True)
        subprocess.run(["git", "pull"], cwd=repo_path, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        console.print("[bold red]Failed to sync with master branch.[/]")
        console.print(e.stderr.decode())
        raise typer.Exit(code=1)

    # 2. Create and checkout the new branch
    console.print(f"[cyan]Creating branch '{branch_name}'...[/]")
    try:
        subprocess.run(["git", "checkout", "-b", branch_name], cwd=repo_path, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Failed to create branch '{branch_name}'.[/]")
        console.print(e.stderr.decode())
        raise typer.Exit(code=1)

    # 3. Create empty commit & push to allow draft PR creation
    console.print("[cyan]Making empty initial commit and pushing to origin...[/]")
    try:
        subprocess.run(["git", "commit", "--allow-empty", "-m", f"Initial draft PR commit for issues: {issue_ids}"], cwd=repo_path, check=True, capture_output=True)
        subprocess.run(["git", "push", "--set-upstream", "origin", branch_name], cwd=repo_path, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        console.print("[bold red]Failed to commit or push upstream branch.[/]")
        console.print(e.stderr.decode())
        # Clean up by checking out master and deleting the branch locally
        subprocess.run(["git", "checkout", "master"], cwd=repo_path, capture_output=True)
        subprocess.run(["git", "branch", "-D", branch_name], cwd=repo_path, capture_output=True)
        raise typer.Exit(code=1)

    # 4. Create draft PR
    console.print("[cyan]Creating draft Pull Request on GitHub...[/]")
    title = f"Draft: branch {branch_name} for issues {issue_ids}"
    body = f"Resolves local issues: {issue_ids}"
    
    try:
        result = subprocess.run([
            "gh", "pr", "create",
            "--draft",
            "--title", title,
            "--body", body
        ], cwd=repo_path, capture_output=True, text=True, check=True)
        
        pr_url = result.stdout.strip()
        console.print(f"[green]Draft PR created successfully:[/] {pr_url}")
    except subprocess.CalledProcessError as e:
        console.print("[bold red]Failed to create draft PR via gh CLI.[/]")
        console.print(e.stderr)
        raise typer.Exit(code=1)

    # 5. Log branch and PR info to database for each issue
    if 'issues' in DB.table_names():
        for i in ids:
            try:
                DB["issues"].update(i, {"branch_name": branch_name, "pr_url": pr_url})
                console.print(f"[green]Logged branch & PR to local issue ID {i}[/]")
            except Exception as e:
                console.print(f"[bold red]Failed to update issue ID {i} in database:[/] {e}")

if __name__ == "__main__":
    app()
