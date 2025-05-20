from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class ShipyardTransferEvent(JournalEvent):
    Distance: Optional[Any] = None
    MarketID: Optional[Any] = None
    ShipID: Optional[Any] = None
    ShipMarketID: Optional[Any] = None
    ShipType: Optional[Any] = None
    ShipType_Localised: Optional[Any] = None
    System: Optional[Any] = None
    TransferPrice: Optional[Any] = None
    TransferTime: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            Distance=data.get('Distance'),
            MarketID=data.get('MarketID'),
            ShipID=data.get('ShipID'),
            ShipMarketID=data.get('ShipMarketID'),
            ShipType=data.get('ShipType'),
            ShipType_Localised=data.get('ShipType_Localised'),
            System=data.get('System'),
            TransferPrice=data.get('TransferPrice'),
            TransferTime=data.get('TransferTime'),
        )
