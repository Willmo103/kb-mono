# /// script
# requires-python = ">=3.13"
# dependencies = ["sqlite-utils", "typer", "rich"]
# ///
import sqlite_utils
from pathlib import Path
import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(help="Search development/agent notes in the local database")
console = Console()

DB_PATH = Path(__file__).parent.parent / 'artifacts.db'
DB = sqlite_utils.Database(DB_PATH)

@app.command()
def search_notes(
    query: str = typer.Argument(None, help="Text query to search for inside title/content"),
    tag: str = typer.Option(None, "--tag", "-t", help="Filter notes by tag")
):
    """
    Searches the agent_notes table in artifacts.db for matching records.
    """
    if 'agent_notes' not in DB.table_names():
        console.print("[bold red]Error:[/] The 'agent_notes' table does not exist in artifacts.db.")
        raise typer.Exit(code=1)

    sql = "select * from agent_notes where 1=1"
    params = []

    if query:
        sql += " and (title like ? or content like ?)"
        like_query = f"%{query}%"
        params.extend([like_query, like_query])
    
    if tag:
        sql += " and tags like ?"
        params.append(f"%{tag}%")

    rows = DB.execute_returning_dicts(sql, params)

    if not rows:
        console.print("[yellow]No matching notes found.[/]")
        return

    console.print(f"[bold green]Found {len(rows)} matching note(s):[/]\n")
    for row in rows:
        console.print(Panel(
            row.get("content", ""),
            title=f"[bold cyan]ID {row.get('id')}: {row.get('title')}[/]",
            subtitle=f"[yellow]Tags: {row.get('tags', '')}[/] | [dim]{row.get('created_at', '')}[/]",
            title_align="left",
            subtitle_align="right"
        ))

if __name__ == "__main__":
    app()
