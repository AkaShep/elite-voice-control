from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class UndockedEvent(JournalEvent):
    MarketID: Optional[Any] = None
    Multicrew: Optional[Any] = None
    StationName: Optional[Any] = None
    StationType: Optional[Any] = None
    Taxi: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            MarketID=data.get('MarketID'),
            Multicrew=data.get('Multicrew'),
            StationName=data.get('StationName'),
            StationType=data.get('StationType'),
            Taxi=data.get('Taxi'),
        )
