import importlib
import pkgutil
from .event_base import JournalEvent

# Папка для автопоиска событий
EVENTS_PKG = "integration.events"

# Собираем все Event-классы в папке events/
EVENT_MAP = {}

for _, module_name, _ in pkgutil.iter_modules(__import__(EVENTS_PKG, fromlist=['']).__path__):
    mod = importlib.import_module(f"{EVENTS_PKG}.{module_name}")
    # Ищем классы, унаследованные от JournalEvent
    for attr in dir(mod):
        obj = getattr(mod, attr)
        if isinstance(obj, type) and issubclass(obj, JournalEvent) and obj is not JournalEvent:
            # Имя события = имя класса без суффикса "Event"
            event_name = attr[:-5] if attr.endswith("Event") else attr
            EVENT_MAP[event_name] = obj

def parse_event(data: dict):
    event_type = data.get("event")
    event_cls = EVENT_MAP.get(event_type)
    if event_cls:
        return event_cls.from_dict(data)
    return None
