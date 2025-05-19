from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from integration.journal.event_base import JournalEvent

@dataclass
class StatisticsEvent(JournalEvent):
    Bank_Account: Optional[Any] = None
    Combat: Optional[Any] = None
    Crafting: Optional[Any] = None
    Crew: Optional[Any] = None
    Crime: Optional[Any] = None
    Exobiology: Optional[Any] = None
    Exploration: Optional[Any] = None
    Material_Trader_Stats: Optional[Any] = None
    Mining: Optional[Any] = None
    Multicrew: Optional[Any] = None
    Passengers: Optional[Any] = None
    Search_And_Rescue: Optional[Any] = None
    Smuggling: Optional[Any] = None
    Trading: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            timestamp=data.get("timestamp"),
            event=data.get("event"),
            Bank_Account=data.get('Bank_Account'),
            Combat=data.get('Combat'),
            Crafting=data.get('Crafting'),
            Crew=data.get('Crew'),
            Crime=data.get('Crime'),
            Exobiology=data.get('Exobiology'),
            Exploration=data.get('Exploration'),
            Material_Trader_Stats=data.get('Material_Trader_Stats'),
            Mining=data.get('Mining'),
            Multicrew=data.get('Multicrew'),
            Passengers=data.get('Passengers'),
            Search_And_Rescue=data.get('Search_And_Rescue'),
            Smuggling=data.get('Smuggling'),
            Trading=data.get('Trading'),
        )
