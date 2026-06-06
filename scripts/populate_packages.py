# /// script
# requires-python = ">=3.13"
# dependencies = ["sqlite-utils"]
# ///
import os
import subprocess
from pathlib import Path
import sqlite_utils
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / 'artifacts.db'
DB = sqlite_utils.Database(DB_PATH)

def populate():
    print("Populating remotes_index table...")
    remotes_dir = Path(__file__).parent.parent / 'remotes'
    
    if not remotes_dir.exists():
        print(f"Directory not found: {remotes_dir}")
        return

    for item in remotes_dir.iterdir():
        if item.is_dir() and (item / '.git').exists() or item.is_dir() and (item.parent.parent / '.gitmodules').exists():
            # Gather info
            name = item.name
            full_path = str(item.resolve())
            rel_path = f"remotes/{name}"
            
            # Get remote URL
            remote_url = ""
            try:
                remote_url = subprocess.check_output(
                    ['git', 'config', '--get', 'remote.origin.url'], 
                    cwd=item, text=True
                ).strip()
            except Exception:
                pass
            
            # Insert into database
            DB['remotes_index'].upsert({
                'name': name,
                'full_path': full_path,
                'rel_path': rel_path,
                'remote_url': remote_url,
                'last_commit': datetime.now().isoformat()
            }, pk='name')

if __name__ == "__main__":
    populate()
    print("Done populating remotes.")
