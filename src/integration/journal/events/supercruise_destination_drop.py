from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class SupercruiseDestinationDropEvent(JournalEvent):
    MarketID: Optional[Any] = None
    Threat: Optional[Any] = None
    Type: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            MarketID=data.get('MarketID'),
            Threat=data.get('Threat'),
            Type=data.get('Type'),
        )
