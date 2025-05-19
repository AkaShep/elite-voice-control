from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class CargoEvent(JournalEvent):
    Count: Optional[Any] = None
    Inventory: Optional[Any] = None
    Vessel: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            Count=data.get('Count'),
            Inventory=data.get('Inventory'),
            Vessel=data.get('Vessel'),
        )
