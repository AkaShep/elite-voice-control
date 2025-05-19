from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class MissionsEvent(JournalEvent):
    Active: Optional[Any] = None
    Complete: Optional[Any] = None
    Failed: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            Active=data.get('Active'),
            Complete=data.get('Complete'),
            Failed=data.get('Failed'),
        )
