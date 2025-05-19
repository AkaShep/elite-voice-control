from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class NpcCrewPaidWageEvent(JournalEvent):
    Amount: Optional[Any] = None
    NpcCrewId: Optional[Any] = None
    NpcCrewName: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            Amount=data.get('Amount'),
            NpcCrewId=data.get('NpcCrewId'),
            NpcCrewName=data.get('NpcCrewName'),
        )
