from dataclasses import dataclass
from typing import Optional
from integration.journal.event_base import JournalEvent

@dataclass
class LocationEvent(JournalEvent):
    StarSystem: Optional[str] = None
    Body: Optional[str] = None
    Docked: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            StarSystem=data.get("StarSystem"),
            Body=data.get("Body"),
            Docked=data.get("Docked"),
        )
