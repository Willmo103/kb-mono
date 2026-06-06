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

app = typer.Typer(help="List git commit history for submodules")
console = Console()

DB_PATH = Path(__file__).parent.parent / 'artifacts.db'
DB = sqlite_utils.Database(DB_PATH)

@app.command()
def get_commits(
    repo: str = typer.Option(None, "--repo", "-r", help="Specify a package name, e.g., kb-web"),
    limit: int = typer.Option(5, "--limit", "-n", help="Number of commits to show per package")
):
    """
    Shows git commit history for one or all packages under the remotes directory.
    """
    remotes_dir = Path(__file__).parent.parent / "remotes"
    if not remotes_dir.exists():
        console.print("[bold red]Error:[/] remotes/ directory does not exist.")
        raise typer.Exit(code=1)

    targets = []
    if repo:
        repo_path = remotes_dir / repo
        if not repo_path.exists() or not repo_path.is_dir():
            console.print(f"[bold red]Error:[/] Repository '{repo}' not found.")
            raise typer.Exit(code=1)
        targets.append(repo_path)
    else:
        # Get all sub directories with git
        for path in sorted(remotes_dir.iterdir()):
            if path.is_dir() and (path / ".git").exists():
                targets.append(path)

    for target_path in targets:
        console.print(f"\n[bold magenta]Recent commits for: {target_path.name}[/]")
        try:
            # git log -n limit --oneline --decorate
            result = subprocess.run(
                ["git", "log", f"-n", str(limit), "--pretty=format:%h - %an, %ar : %s"],
                cwd=target_path, capture_output=True, text=True, check=True
            )
            commits = result.stdout.strip()
            if commits:
                for line in commits.split("\n"):
                    console.print(f"  {line}")
            else:
                console.print("  [yellow]No commits found.[/]")
        except subprocess.CalledProcessError as e:
            console.print(f"  [red]Error reading commits:[/] {e.stderr.strip()}")

if __name__ == "__main__":
    app()
