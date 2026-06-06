# /// script
# requires-python = ">=3.13"
# dependencies = ["sqlite-utils", "typer", "rich"]
# ///
import sqlite_utils
from pathlib import Path
import subprocess
import typer
from rich.console import Console

app = typer.Typer(help="Get git diffs for a submodule repository")
console = Console()

DB_PATH = Path(__file__).parent.parent / 'artifacts.db'
DB = sqlite_utils.Database(DB_PATH)

@app.command()
def get_diffs(
    repo: str = typer.Argument(..., help="The package name, e.g., kb-web"),
    cached: bool = typer.Option(False, "--cached", "-c", help="Show staged changes diff")
):
    """
    Shows a colored, friendly git diff of modified/staged files in a package.
    """
    repo_path = Path(__file__).parent.parent / "remotes" / repo
    
    if not repo_path.exists() or not repo_path.is_dir():
        console.print(f"[bold red]Error:[/] Repository {repo} not found in remotes/")
        raise typer.Exit(code=1)

    cmd = ["git", "diff", "--color=always"]
    if cached:
        cmd.append("--cached")

    try:
        result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True, check=True)
        diff_output = result.stdout.strip()
        if diff_output:
            console.print(diff_output)
        else:
            console.print(f"[yellow]No modifications found in '{repo}' Working Directory (cached={cached}).[/]")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Failed to get git diff for {repo}.[/]")
        console.print(e.stderr)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
