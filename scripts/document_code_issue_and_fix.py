# /// script
# requires-python = ">=3.13"
# dependencies = ["sqlite-utils", "typer", "rich"]
# ///
import sqlite_utils
from pathlib import Path
from datetime import datetime
import typer
from rich.console import Console

app = typer.Typer(help="Document a specific code issue and its corresponding fix")
console = Console()

DB_PATH = Path(__file__).parent.parent / 'artifacts.db'
DB = sqlite_utils.Database(DB_PATH)

def read_input_or_file(val: str) -> str:
    """Helper to read from a file if the value points to an existing file, otherwise returns string."""
    if not val:
        return ""
    try:
        path = Path(val)
        if path.is_file():
            return path.read_text(encoding='utf-8')
    except Exception:
        pass
    return val

@app.command()
def document(
    issue: str = typer.Argument(..., help="Short title/summary of the issue"),
    description: str = typer.Argument(..., help="Detailed description of the bug or symptom"),
    code_before: str = typer.Option("", "--before", "-b", help="File path or code block representing the broken code"),
    code_after: str = typer.Option("", "--after", "-a", help="File path or code block representing the fixed code"),
    explanation: str = typer.Option("", "--explanation", "-e", help="Short summary of why this change fixed the bug")
):
    """
    Saves a code fix entry to code_fixes table in artifacts.db.
    """
    if 'code_fixes' not in DB.table_names():
        console.print("[bold red]Error:[/] The 'code_fixes' table does not exist in artifacts.db.")
        raise typer.Exit(code=1)

    before_content = read_input_or_file(code_before)
    after_content = read_input_or_file(code_after)

    fix_data = {
        "issue": issue,
        "description": description,
        "code_before": before_content,
        "code_after": after_content,
        "fix_explanation": explanation,
        "created_at": datetime.now().isoformat()
    }

    try:
        inserted_id = DB["code_fixes"].insert(fix_data).last_pk
        console.print(f"[green]✔ Successfully documented code fix (ID: {inserted_id}) in artifacts.db.[/]")
    except Exception as e:
        console.print(f"[bold red]Failed to save code fix to database:[/] {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
