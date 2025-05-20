from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class ShipyardEvent(JournalEvent):
    MarketID: Optional[Any] = None
    StarSystem: Optional[Any] = None
    StationName: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            MarketID=data.get('MarketID'),
            StarSystem=data.get('StarSystem'),
            StationName=data.get('StationName'),
        )
