from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class LoadoutEvent(JournalEvent):
    Ship: Optional[str] = None
    ShipID: Optional[int] = None
    ShipName: Optional[str] = None
    Modules: Optional[List[Dict[str, Any]]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            Ship=data.get("Ship"),
            ShipID=data.get("ShipID"),
            ShipName=data.get("ShipName"),
            Modules=data.get("Modules", []),
        )
