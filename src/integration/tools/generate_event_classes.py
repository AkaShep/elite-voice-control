import json
import keyword
import re
from pathlib import Path
from collections import defaultdict

LOGS_DIR = Path.home() / "Saved Games" / "Frontier Developments" / "Elite Dangerous"
EVENTS_DIR = Path(__file__).parent.parent / "journal" / "events"

def to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def fix_field(name):
    if keyword.iskeyword(name):
        return name + "_"
    name = name.replace("-", "_")
    name = name.replace(" ", "_")
    return name

event_fields = defaultdict(set)

for file in LOGS_DIR.glob("Journal*.log"):
    with open(file, encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                event = data.get("event")
                if event:
                    for k in data:
                        if k not in ("timestamp", "event"):
                            event_fields[event].add(k)
            except Exception:
                continue

base = '''from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class {class_name}(JournalEvent):
{fields}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
{kwargs}
        )
'''

EVENTS_DIR.mkdir(exist_ok=True)

skipped, written = 0, 0
for event, fields in event_fields.items():
    class_name = event + "Event"
    file_name = to_snake_case(event) + ".py"
    path = EVENTS_DIR / file_name
    if path.exists():
        skipped += 1
        continue  # Не перезаписывать существующий файл!
    lines = []
    kwargs_lines = []

    for field in sorted(fields):
        safe_field = fix_field(field)
        lines.append(f"    {safe_field}: Optional[Any] = None")
        kwargs_lines.append(f"            {safe_field}=data.get('{field}'),")
    fields_code = "\n".join(lines)
    kwargs_code = "\n".join(kwargs_lines)

    code = base.format(class_name=class_name, fields=fields_code, kwargs=kwargs_code)
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    written += 1

print(f"Сгенерировано {written} новых событий, пропущено (уже есть): {skipped}. Папка: {EVENTS_DIR}")
