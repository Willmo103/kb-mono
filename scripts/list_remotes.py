# /// script
# requires-python = ">=3.13"
# dependencies = ["sqlite-utils"]
# ///
import sqlite_utils
from pathlib import Path
from populate_packages import populate

DB_PATH = Path(__file__).parent.parent / 'artifacts.db'
DB = sqlite_utils.Database(DB_PATH)

def main():
    if 'remotes_index' not in DB.table_names() or DB['remotes_index'].count == 0:
        populate()

    rows = DB.execute_returning_dicts('select * from remotes_index')
    for row in rows:
        header = '-' * 10 + f' ID: {row["id"]} ' + '-' * 10
        print(header)
        print(f"Name: {row['name']}")
        print(f"Full Path: {row['full_path']}")
        print(f"Workspace Path: {row['rel_path']}")
        print(f"Remote URL: `{row['remote_url']}`")
        print(f"Last Commit Timestamp: {row['last_commit']}")
        print('-' * len(header))

if __name__ == "__main__":
    main()
