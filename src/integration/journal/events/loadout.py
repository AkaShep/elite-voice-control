from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class LoadoutEvent(JournalEvent):
    CargoCapacity: Optional[Any] = None
    FuelCapacity: Optional[Any] = None
    Hot: Optional[Any] = None
    HullHealth: Optional[Any] = None
    HullValue: Optional[Any] = None
    MaxJumpRange: Optional[Any] = None
    Modules: Optional[Any] = None
    ModulesValue: Optional[Any] = None
    Rebuy: Optional[Any] = None
    Ship: Optional[Any] = None
    ShipID: Optional[Any] = None
    ShipIdent: Optional[Any] = None
    ShipName: Optional[Any] = None
    UnladenMass: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            CargoCapacity=data.get('CargoCapacity'),
            FuelCapacity=data.get('FuelCapacity'),
            Hot=data.get('Hot'),
            HullHealth=data.get('HullHealth'),
            HullValue=data.get('HullValue'),
            MaxJumpRange=data.get('MaxJumpRange'),
            Modules=data.get('Modules'),
            ModulesValue=data.get('ModulesValue'),
            Rebuy=data.get('Rebuy'),
            Ship=data.get('Ship'),
            ShipID=data.get('ShipID'),
            ShipIdent=data.get('ShipIdent'),
            ShipName=data.get('ShipName'),
            UnladenMass=data.get('UnladenMass'),
        )
