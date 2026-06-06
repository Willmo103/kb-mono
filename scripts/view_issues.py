# /// script
# requires-python = ">=3.13"
# dependencies = ["sqlite-utils", "typer", "rich"]
# ///
import sqlite_utils
from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="View logged issues in artifacts.db")
console = Console()

DB_PATH = Path(__file__).parent.parent / 'artifacts.db'
DB = sqlite_utils.Database(DB_PATH)

@app.command()
def view_issues(
    repo: str = typer.Option(None, "--repo", "-r", help="Filter by repository package name"),
    label: str = typer.Option(None, "--label", "-l", help="Filter by label")
):
    """
    Displays a list of issues from the artifacts.db database.
    """
    if 'issues' not in DB.table_names():
        console.print("[bold red]Error:[/] The 'issues' table does not exist in artifacts.db.")
        raise typer.Exit(code=1)

    query = "select * from issues where 1=1"
    params = []
    if repo:
        query += " and repo = ?"
        params.append(repo)
    if label:
        query += " and label = ?"
        params.append(label)

    rows = DB.execute_returning_dicts(query, params)

    if not rows:
        console.print("[yellow]No issues found matching the criteria.[/]")
        return

    table = Table(title="Logged Issues")
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Repo", style="magenta")
    table.add_column("Title", style="green")
    table.add_column("Label", style="yellow")
    table.add_column("Project", style="blue")
    table.add_column("Change ID", justify="right")

    for row in rows:
        table.add_row(
            str(row.get("id")),
            row.get("repo", ""),
            row.get("title", ""),
            row.get("label", ""),
            row.get("project", ""),
            str(row.get("change_id") or "")
        )

    console.print(table)

if __name__ == "__main__":
    app()
