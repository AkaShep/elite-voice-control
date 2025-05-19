from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class PowerplayEvent(JournalEvent):
    Merits: Optional[Any] = None
    Power: Optional[Any] = None
    Rank: Optional[Any] = None
    TimePledged: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            Merits=data.get('Merits'),
            Power=data.get('Power'),
            Rank=data.get('Rank'),
            TimePledged=data.get('TimePledged'),
        )
