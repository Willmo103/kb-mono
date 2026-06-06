# /// script
# requires-python = ">=3.13"
# dependencies = ["sqlite-utils", "typer", "rich"]
# ///
import sqlite_utils
from pathlib import Path
from datetime import datetime
import typer
from rich.console import Console

app = typer.Typer(help="Add a developer/agent note to the local database")
console = Console()

DB_PATH = Path(__file__).parent.parent / 'artifacts.db'
DB = sqlite_utils.Database(DB_PATH)

@app.command()
def add_note(
    title: str = typer.Argument(..., help="Title of the note"),
    content: str = typer.Argument(..., help="Detailed content or markdown description of the note"),
    tags: str = typer.Option("", "--tags", "-t", help="Comma-separated tags for categorizing the note")
):
    """
    Saves a development note into the agent_notes table in artifacts.db.
    """
    if 'agent_notes' not in DB.table_names():
        console.print("[bold red]Error:[/] The 'agent_notes' table does not exist in artifacts.db.")
        raise typer.Exit(code=1)

    note_data = {
        "title": title,
        "content": content,
        "tags": tags,
        "created_at": datetime.now().isoformat()
    }

    try:
        inserted_id = DB["agent_notes"].insert(note_data).last_pk
        console.print(f"[green]✔ Successfully added note (ID: {inserted_id}) to artifacts.db.[/]")
    except Exception as e:
        console.print(f"[bold red]Failed to save note to database:[/] {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
