from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class ShipLockerEvent(JournalEvent):
    Items: Optional[List[Dict[str, Any]]] = field(default_factory=list)
    Components: Optional[List[Dict[str, Any]]] = field(default_factory=list)
    Consumables: Optional[List[Dict[str, Any]]] = field(default_factory=list)
    Data: Optional[List[Dict[str, Any]]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            Items=data.get("Items", []),
            Components=data.get("Components", []),
            Consumables=data.get("Consumables", []),
            Data=data.get("Data", []),
        )
