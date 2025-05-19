from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class SupercruiseExitEvent(JournalEvent):
    Body: Optional[Any] = None
    BodyID: Optional[Any] = None
    BodyType: Optional[Any] = None
    Multicrew: Optional[Any] = None
    StarSystem: Optional[Any] = None
    SystemAddress: Optional[Any] = None
    Taxi: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            Body=data.get('Body'),
            BodyID=data.get('BodyID'),
            BodyType=data.get('BodyType'),
            Multicrew=data.get('Multicrew'),
            StarSystem=data.get('StarSystem'),
            SystemAddress=data.get('SystemAddress'),
            Taxi=data.get('Taxi'),
        )
