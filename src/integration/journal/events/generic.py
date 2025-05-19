from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from integration.journal.event_base import JournalEvent

@dataclass
class GenericJournalEvent(JournalEvent):
    data: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            data={k: v for k, v in data.items() if k not in {"timestamp", "event"}}
        )
