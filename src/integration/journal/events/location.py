from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class LocationEvent(JournalEvent):
    Body: Optional[Any] = None
    BodyID: Optional[Any] = None
    BodyType: Optional[Any] = None
    Conflicts: Optional[Any] = None
    ControllingPower: Optional[Any] = None
    DistFromStarLS: Optional[Any] = None
    Docked: Optional[Any] = None
    Factions: Optional[Any] = None
    MarketID: Optional[Any] = None
    Multicrew: Optional[Any] = None
    Population: Optional[Any] = None
    PowerplayState: Optional[Any] = None
    PowerplayStateControlProgress: Optional[Any] = None
    PowerplayStateReinforcement: Optional[Any] = None
    PowerplayStateUndermining: Optional[Any] = None
    Powers: Optional[Any] = None
    StarPos: Optional[Any] = None
    StarSystem: Optional[Any] = None
    StationEconomies: Optional[Any] = None
    StationEconomy: Optional[Any] = None
    StationEconomy_Localised: Optional[Any] = None
    StationFaction: Optional[Any] = None
    StationGovernment: Optional[Any] = None
    StationGovernment_Localised: Optional[Any] = None
    StationName: Optional[Any] = None
    StationServices: Optional[Any] = None
    StationType: Optional[Any] = None
    SystemAddress: Optional[Any] = None
    SystemAllegiance: Optional[Any] = None
    SystemEconomy: Optional[Any] = None
    SystemEconomy_Localised: Optional[Any] = None
    SystemFaction: Optional[Any] = None
    SystemGovernment: Optional[Any] = None
    SystemGovernment_Localised: Optional[Any] = None
    SystemSecondEconomy: Optional[Any] = None
    SystemSecondEconomy_Localised: Optional[Any] = None
    SystemSecurity: Optional[Any] = None
    SystemSecurity_Localised: Optional[Any] = None
    Taxi: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            Body=data.get('Body'),
            BodyID=data.get('BodyID'),
            BodyType=data.get('BodyType'),
            Conflicts=data.get('Conflicts'),
            ControllingPower=data.get('ControllingPower'),
            DistFromStarLS=data.get('DistFromStarLS'),
            Docked=data.get('Docked'),
            Factions=data.get('Factions'),
            MarketID=data.get('MarketID'),
            Multicrew=data.get('Multicrew'),
            Population=data.get('Population'),
            PowerplayState=data.get('PowerplayState'),
            PowerplayStateControlProgress=data.get('PowerplayStateControlProgress'),
            PowerplayStateReinforcement=data.get('PowerplayStateReinforcement'),
            PowerplayStateUndermining=data.get('PowerplayStateUndermining'),
            Powers=data.get('Powers'),
            StarPos=data.get('StarPos'),
            StarSystem=data.get('StarSystem'),
            StationEconomies=data.get('StationEconomies'),
            StationEconomy=data.get('StationEconomy'),
            StationEconomy_Localised=data.get('StationEconomy_Localised'),
            StationFaction=data.get('StationFaction'),
            StationGovernment=data.get('StationGovernment'),
            StationGovernment_Localised=data.get('StationGovernment_Localised'),
            StationName=data.get('StationName'),
            StationServices=data.get('StationServices'),
            StationType=data.get('StationType'),
            SystemAddress=data.get('SystemAddress'),
            SystemAllegiance=data.get('SystemAllegiance'),
            SystemEconomy=data.get('SystemEconomy'),
            SystemEconomy_Localised=data.get('SystemEconomy_Localised'),
            SystemFaction=data.get('SystemFaction'),
            SystemGovernment=data.get('SystemGovernment'),
            SystemGovernment_Localised=data.get('SystemGovernment_Localised'),
            SystemSecondEconomy=data.get('SystemSecondEconomy'),
            SystemSecondEconomy_Localised=data.get('SystemSecondEconomy_Localised'),
            SystemSecurity=data.get('SystemSecurity'),
            SystemSecurity_Localised=data.get('SystemSecurity_Localised'),
            Taxi=data.get('Taxi'),
        )
