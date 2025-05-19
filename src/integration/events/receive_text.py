from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class ReceiveTextEvent(JournalEvent):
    Channel: Optional[Any] = None
    From: Optional[Any] = None
    From_Localised: Optional[Any] = None
    Message: Optional[Any] = None
    Message_Localised: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            Channel=data.get('Channel'),
            From=data.get('From'),
            From_Localised=data.get('From_Localised'),
            Message=data.get('Message'),
            Message_Localised=data.get('Message_Localised'),
        )
