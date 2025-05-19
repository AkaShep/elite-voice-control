from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class FSSSignalDiscoveredEvent(JournalEvent):
    IsStation: Optional[Any] = None
    SignalName: Optional[Any] = None
    SignalName_Localised: Optional[Any] = None
    SignalType: Optional[Any] = None
    SystemAddress: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            IsStation=data.get('IsStation'),
            SignalName=data.get('SignalName'),
            SignalName_Localised=data.get('SignalName_Localised'),
            SignalType=data.get('SignalType'),
            SystemAddress=data.get('SystemAddress'),
        )
