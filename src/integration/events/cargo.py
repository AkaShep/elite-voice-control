from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class CargoEvent(JournalEvent):
    Vessel: Optional[str] = None
    Count: Optional[int] = None
    Inventory: Optional[List[Dict[str, Any]]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            Vessel=data.get("Vessel"),
            Count=data.get("Count"),
            Inventory=data.get("Inventory", []),
        )
