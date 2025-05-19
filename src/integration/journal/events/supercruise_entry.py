from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class SupercruiseEntryEvent(JournalEvent):
    Multicrew: Optional[Any] = None
    StarSystem: Optional[Any] = None
    SystemAddress: Optional[Any] = None
    Taxi: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            Multicrew=data.get('Multicrew'),
            StarSystem=data.get('StarSystem'),
            SystemAddress=data.get('SystemAddress'),
            Taxi=data.get('Taxi'),
        )
