import json
import keyword
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import time
import threading
import sys

LOGS_DIR = Path.home() / "Saved Games" / "Frontier Developments" / "Elite Dangerous"
EVENTS_DIR = Path(__file__).parent.parent / "journal" / "events"
LOG_FILE = Path(__file__).parent / "generate_event_classes.log"

def to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def fix_field(name):
    if keyword.iskeyword(name):
        return name + "_"
    name = name.replace("-", "_")
    name = name.replace(" ", "_")
    return name

def generate_event_class(event, fields):
    class_name = event + "Event"
    file_name = to_snake_case(event) + ".py"
    path = EVENTS_DIR / file_name
    if path.exists():
        return None
    lines = []
    kwargs_lines = []
    for field in sorted(fields):
        safe_field = fix_field(field)
        lines.append(f"    {safe_field}: Optional[Any] = None")
        kwargs_lines.append(f"            {safe_field}=data.get('{field}'),")
    fields_code = "\n".join(lines)
    kwargs_code = "\n".join(kwargs_lines)

    code = f'''from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class {class_name}(JournalEvent):
{fields_code}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
{kwargs_code}
        )
'''
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    return class_name

def log_event_addition(added_events):
    LOG_FILE.parent.mkdir(exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as logf:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if added_events:
            logf.write(f"[{now}] Добавлены новые события: {', '.join(added_events)}\n")

def monitor_journal_files(poll_interval=2.0):
    EVENTS_DIR.mkdir(exist_ok=True)
    known_events = set([f.stem.replace("_event", "") for f in EVENTS_DIR.glob("*.py")])
    known_fields = defaultdict(set)
    # Сохраняем позиции файлов (чтобы читать только новые строки)
    positions = {}

    print("Мониторинг журналов Elite Dangerous на новые типы событий...")
    while True:
        added_events = []
        for file in LOGS_DIR.glob("Journal*.log"):
            # Инициализация позиции
            if file not in positions:
                positions[file] = 0
            try:
                with open(file, encoding="utf-8") as f:
                    f.seek(positions[file])
                    for line in f:
                        data = None
                        try:
                            data = json.loads(line)
                        except Exception:
                            continue
                        event = data.get("event")
                        if not event or event.lower() == "fileheader":
                            continue
                        if event not in known_events:
                            fields = set(data.keys()) - {"timestamp", "event"}
                            generated = generate_event_class(event, fields)
                            if generated:
                                added_events.append(generated)
                                known_events.add(event)
                                print(f"[+] Новый тип события: {event}")
                        # Можно также обновлять поля для уже известных событий
                    positions[file] = f.tell()
            except Exception as e:
                print(f"[!] Ошибка чтения журнала: {e}")

        if added_events:
            log_event_addition(added_events)
        time.sleep(poll_interval)

if __name__ == "__main__":
    try:
        monitor_journal_files()
    except KeyboardInterrupt:
        print("Мониторинг завершён.")
        sys.exit(0)
