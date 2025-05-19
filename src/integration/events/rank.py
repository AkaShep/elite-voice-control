from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class RankEvent(JournalEvent):
    CQC: Optional[Any] = None
    Combat: Optional[Any] = None
    Empire: Optional[Any] = None
    Exobiologist: Optional[Any] = None
    Explore: Optional[Any] = None
    Federation: Optional[Any] = None
    Soldier: Optional[Any] = None
    Trade: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            CQC=data.get('CQC'),
            Combat=data.get('Combat'),
            Empire=data.get('Empire'),
            Exobiologist=data.get('Exobiologist'),
            Explore=data.get('Explore'),
            Federation=data.get('Federation'),
            Soldier=data.get('Soldier'),
            Trade=data.get('Trade'),
        )
