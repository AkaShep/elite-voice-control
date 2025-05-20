from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class RefuelAllEvent(JournalEvent):
    Amount: Optional[Any] = None
    Cost: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            Amount=data.get('Amount'),
            Cost=data.get('Cost'),
        )
