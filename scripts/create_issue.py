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

app = typer.Typer(help="Create a draft issue in GitHub and log it to artifacts.db")
console = Console()

DB_PATH = Path(__file__).parent.parent / 'artifacts.db'
DB = sqlite_utils.Database(DB_PATH)

@app.command()
def create_issue(
    repo: str = typer.Argument(..., help="The package name, e.g., kb-web"),
    title: str = typer.Argument(..., help="Title of the issue"),
    message: str = typer.Argument(..., help="Body of the issue"),
    label: str = typer.Option("feature", "--label", "-l", help="Issue label"),
    project: str = typer.Option("kb-mono CICD", "--project", "-p", help="GitHub Project name"),
    change_id: int = typer.Option(None, "--change-id", "-c", help="Optional change ID from the changes table")
):
    """
    Creates an issue on GitHub using the 'gh' CLI and logs it into the local SQLite database.
    """
    repo_path = Path(__file__).parent.parent / "remotes" / repo
    
    if not repo_path.exists() or not repo_path.is_dir():
        console.print(f"[bold red]Error:[/] Repository {repo} not found in remotes/")
        raise typer.Exit(code=1)
    
    # Verify 'gh' CLI is installed
    try:
        subprocess.run(["gh", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        console.print("[bold red]Error:[/] The GitHub CLI ('gh') is not installed or not in PATH.")
        raise typer.Exit(code=1)
        
    console.print(f"[cyan]Creating issue in {repo}...[/]")
    
    # Run gh issue create
    try:
        result = subprocess.run([
            "gh", "issue", "create",
            "--title", title,
            "--body", message,
            "--label", label,
            "--project", project
        ], cwd=repo_path, capture_output=True, text=True, check=True)
        
        issue_url = result.stdout.strip()
        console.print(f"[green]Successfully created issue:[/] {issue_url}")
        
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Failed to create issue via gh CLI.[/]")
        console.print(e.stderr)
        raise typer.Exit(code=1)

    # Log into database
    issue_data = {
        "repo": repo,
        "title": title,
        "message": message,
        "label": label,
        "project": project,
        "change_id": change_id
    }
    
    # Ensure issues table exists, upsert structure if needed
    if 'issues' not in DB.table_names():
        console.print("[bold yellow]Warning:[/] 'issues' table not found. Please ensure artifacts.db is initialized properly.")
    
    try:
        inserted = DB["issues"].insert(issue_data).last_pk
        console.print(f"[green]Logged issue to artifacts.db with ID:[/] {inserted}")
    except Exception as e:
        console.print(f"[bold red]Failed to log issue to database:[/] {e}")
        
if __name__ == "__main__":
    app()
