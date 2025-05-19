from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class ReservoirReplenishedEvent(JournalEvent):
    FuelMain: Optional[Any] = None
    FuelReservoir: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            FuelMain=data.get('FuelMain'),
            FuelReservoir=data.get('FuelReservoir'),
        )
