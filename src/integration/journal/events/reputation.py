from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class ReputationEvent(JournalEvent):
    Alliance: Optional[Any] = None
    Empire: Optional[Any] = None
    Federation: Optional[Any] = None
    Independent: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            Alliance=data.get('Alliance'),
            Empire=data.get('Empire'),
            Federation=data.get('Federation'),
            Independent=data.get('Independent'),
        )
