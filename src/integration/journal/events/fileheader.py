from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class FileheaderEvent(JournalEvent):
    Odyssey: Optional[Any] = None
    build: Optional[Any] = None
    gameversion: Optional[Any] = None
    language: Optional[Any] = None
    part: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            Odyssey=data.get('Odyssey'),
            build=data.get('build'),
            gameversion=data.get('gameversion'),
            language=data.get('language'),
            part=data.get('part'),
        )
