from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class ModuleStoreEvent(JournalEvent):
    Hot: Optional[Any] = None
    MarketID: Optional[Any] = None
    Ship: Optional[Any] = None
    ShipID: Optional[Any] = None
    Slot: Optional[Any] = None
    StoredItem: Optional[Any] = None
    StoredItem_Localised: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            Hot=data.get('Hot'),
            MarketID=data.get('MarketID'),
            Ship=data.get('Ship'),
            ShipID=data.get('ShipID'),
            Slot=data.get('Slot'),
            StoredItem=data.get('StoredItem'),
            StoredItem_Localised=data.get('StoredItem_Localised'),
        )
