"""
sets the {{ workflow_type }} id.
"""

from datetime import datetime
from pathlib import Path
from uuid import uuid4

NEW_{{ workflow_type | upper }}_ID_PATH = Path(__file__).parent.parent / "_new_{{ workflow_type }}_id"
ARTIFACTS_{{ workflow_type | upper }}_DIR = Path(__file__).parent.parent / "artifacts" / "{{ workflow_type }}"

NEW_{{ workflow_type | upper }}_ID = f"{datetime.now().strftime('%m%d%y')}-{uuid4().hex[:8]}"
NEW_{{ workflow_type | upper }}_ID_PATH.write_text(NEW_{{ workflow_type | upper }}_ID)
(ARTIFACTS_{{ workflow_type | upper }}_DIR / f"{NEW_{{ workflow_type | upper }}_ID}").mkdir(parents=True, exist_ok=True)
print(f"Id: {{new_{{ workflow_type | upper }}_id}}")
