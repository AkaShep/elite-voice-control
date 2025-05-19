# базовый класс события
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class JournalEvent:
    timestamp: Optional[str]
    event: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
