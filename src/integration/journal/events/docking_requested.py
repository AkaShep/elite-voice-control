from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class DockingRequestedEvent(JournalEvent):
    LandingPads: Optional[Any] = None
    MarketID: Optional[Any] = None
    StationName: Optional[Any] = None
    StationType: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            LandingPads=data.get('LandingPads'),
            MarketID=data.get('MarketID'),
            StationName=data.get('StationName'),
            StationType=data.get('StationType'),
        )
