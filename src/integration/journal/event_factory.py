import importlib
import pkgutil
import inspect
from integration.journal.event_base import JournalEvent
from integration.journal.events.generic import GenericJournalEvent

EVENTS_PKG = "integration.journal.events"

# Собираем все Event-классы в папке events/
EVENT_MAP = {}

pkg = importlib.import_module(EVENTS_PKG)
for _, module_name, is_pkg in pkgutil.iter_modules(pkg.__path__):
    if is_pkg:
        continue  # пропуск подпакетов
    mod = importlib.import_module(f"{EVENTS_PKG}.{module_name}")
    for name, obj in inspect.getmembers(mod):
        if (
            inspect.isclass(obj)
            and issubclass(obj, JournalEvent)
            and obj is not JournalEvent
            and name.endswith("Event")
        ):
            # Имя события = имя класса без "Event" на конце
            event_name = name[:-5]
            EVENT_MAP[event_name] = obj

def parse_event(data: dict):
    event_type = data.get("event")
    event_cls = EVENT_MAP.get(event_type, GenericJournalEvent)
    return event_cls.from_dict(data)
