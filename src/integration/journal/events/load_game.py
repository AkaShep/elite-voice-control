from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class LoadGameEvent(JournalEvent):
    Commander: Optional[Any] = None
    Credits: Optional[Any] = None
    FID: Optional[Any] = None
    FuelCapacity: Optional[Any] = None
    FuelLevel: Optional[Any] = None
    GameMode: Optional[Any] = None
    Group: Optional[Any] = None
    Horizons: Optional[Any] = None
    Loan: Optional[Any] = None
    Odyssey: Optional[Any] = None
    Ship: Optional[Any] = None
    ShipID: Optional[Any] = None
    ShipIdent: Optional[Any] = None
    ShipName: Optional[Any] = None
    build: Optional[Any] = None
    gameversion: Optional[Any] = None
    language: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            Commander=data.get('Commander'),
            Credits=data.get('Credits'),
            FID=data.get('FID'),
            FuelCapacity=data.get('FuelCapacity'),
            FuelLevel=data.get('FuelLevel'),
            GameMode=data.get('GameMode'),
            Group=data.get('Group'),
            Horizons=data.get('Horizons'),
            Loan=data.get('Loan'),
            Odyssey=data.get('Odyssey'),
            Ship=data.get('Ship'),
            ShipID=data.get('ShipID'),
            ShipIdent=data.get('ShipIdent'),
            ShipName=data.get('ShipName'),
            build=data.get('build'),
            gameversion=data.get('gameversion'),
            language=data.get('language'),
        )
