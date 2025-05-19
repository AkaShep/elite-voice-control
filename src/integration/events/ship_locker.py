from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class ShipLockerEvent(JournalEvent):
    Components: Optional[Any] = None
    Consumables: Optional[Any] = None
    Data: Optional[Any] = None
    Items: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            Components=data.get('Components'),
            Consumables=data.get('Consumables'),
            Data=data.get('Data'),
            Items=data.get('Items'),
        )
