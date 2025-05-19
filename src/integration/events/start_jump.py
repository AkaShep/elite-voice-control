from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class StartJumpEvent(JournalEvent):
    JumpType: Optional[Any] = None
    Taxi: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            JumpType=data.get('JumpType'),
            Taxi=data.get('Taxi'),
        )
