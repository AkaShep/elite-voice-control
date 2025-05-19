from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class MaterialsEvent(JournalEvent):
    Encoded: Optional[Any] = None
    Manufactured: Optional[Any] = None
    Raw: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            Encoded=data.get('Encoded'),
            Manufactured=data.get('Manufactured'),
            Raw=data.get('Raw'),
        )
