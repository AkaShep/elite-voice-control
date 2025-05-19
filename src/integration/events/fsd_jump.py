# пример: FSDJump событие
from dataclasses import dataclass
from typing import Optional
from ..journal.event_base import JournalEvent

@dataclass
class FSDJumpEvent(JournalEvent):
    StarSystem: str
    JumpDist: Optional[float] = None
    FuelUsed: Optional[float] = None
    FuelLevel: Optional[float] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
