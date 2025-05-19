from dataclasses import dataclass
from typing import Optional

@dataclass
class JournalEvent:
    timestamp: Optional[str]
    event: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
