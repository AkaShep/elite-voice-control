import json
from pathlib import Path

journal_dir = Path.home() / "Saved Games" / "Frontier Developments" / "Elite Dangerous"
journal_files = sorted(journal_dir.glob("Journal*.log"))
journal_path = journal_files[-1]  # Самый последний журнал

event = {
    "timestamp": "2025-05-19T21:00:00Z",
    "event": "Docked",
    "StationName": "Test Station"
}

with open(journal_path, "a", encoding="utf-8") as f:
    f.write(json.dumps(event, ensure_ascii=False) + "\n")

print(f"Событие добавлено в {journal_path}")
