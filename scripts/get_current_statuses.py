# /// script
# requires-python = ">=3.13"
# dependencies = ["sqlite-utils", "typer", "rich"]
# ///
import sqlite_utils
from pathlib import Path
import subprocess
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Show the branch and commit status of all submodules")
console = Console()

DB_PATH = Path(__file__).parent.parent / 'artifacts.db'
DB = sqlite_utils.Database(DB_PATH)

@app.command()
def get_statuses():
    """
    Scans the remotes directory and displays a table of checked-out branches
    and working directory cleanliness.
    """
    remotes_dir = Path(__file__).parent.parent / "remotes"
    if not remotes_dir.exists():
        console.print("[bold red]Error:[/] remotes/ directory does not exist.")
        raise typer.Exit(code=1)

    table = Table(title="Package Status Dashboard")
    table.add_column("Package Name", style="magenta")
    table.add_column("Current Branch", style="cyan")
    table.add_column("Status", style="yellow")
    table.add_column("Git Status Summary")

    for path in sorted(remotes_dir.iterdir()):
        if not path.is_dir() or not (path / ".git").exists():
            # Check if submodule folder is empty or not git init
            if path.is_dir():
                table.add_row(path.name, "-", "[red]Not Initialized[/]", "No .git folder found")
            continue

        # Get current branch
        branch = "Unknown"
        try:
            res = subprocess.run(["git", "branch", "--show-current"], cwd=path, capture_output=True, text=True, check=True)
            branch = res.stdout.strip() or "Detached Head / No Branch"
        except subprocess.CalledProcessError:
            pass

        # Check status
        dirty = False
        summary = "Clean"
        try:
            status_res = subprocess.run(["git", "status", "--porcelain"], cwd=path, capture_output=True, text=True, check=True)
            status_out = status_res.stdout.strip()
            if status_out:
                dirty = True
                lines = status_out.split("\n")
                summary = f"{len(lines)} file(s) modified/untracked"
        except subprocess.CalledProcessError:
            summary = "Error running git status"

        status_text = "[bold yellow]Modified[/]" if dirty else "[bold green]Clean[/]"
        table.add_row(path.name, branch, status_text, summary)

    console.print(table)

if __name__ == "__main__":
    app()
