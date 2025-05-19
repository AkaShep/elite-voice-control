from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class CommanderEvent(JournalEvent):
    FID: Optional[Any] = None
    Name: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            FID=data.get('FID'),
            Name=data.get('Name'),
        )
