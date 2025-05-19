from ..events.location import LocationEvent
from ..events.loadout import LoadoutEvent
from ..events.cargo import CargoEvent
from ..events.shiplocker import ShipLockerEvent

EVENT_MAP = {
    "Location": LocationEvent,
    "Loadout": LoadoutEvent,
    "Cargo": CargoEvent,
    "ShipLocker": ShipLockerEvent,
    # Добавляй другие события по мере необходимости
}

def parse_event(data: dict):
    event_type = data.get("event")
    event_cls = EVENT_MAP.get(event_type)
    if event_cls:
        return event_cls.from_dict(data)
    return None
