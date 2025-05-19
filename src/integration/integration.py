# Точка входа, связывает парсер и ассистента
from pathlib import Path
from integration.journal.dispatcher import EventDispatcher
from integration.journal.watcher import JournalWatcher
from integration.journal.event_factory import parse_event
from integration.journal.events.location import LocationEvent
from integration.journal.events.fsd_jump import FSDJumpEvent
from integration.journal.events.targeted import TargetedEvent
from integration.journal.events.hull_damage import HullDamageEvent
from integration.event_handlers import (
    handle_location,
    handle_fsd_jump,
    handle_targeted,
    handle_hull_damage,
)

# Универсальный принтер событий
def print_any_event(event):
    print(f"[{event.event}] {event}")
    print(f"[{event.event}] ({type(event)}) {event}")

def main():
    dispatcher = EventDispatcher()

    # Автоматически подписываемся на все события (универсальный принтер)
    # Можно добавить фильтры, если нужно (например, только важные события)
    from integration.journal.event_base import JournalEvent
    dispatcher.subscribe(JournalEvent, print_any_event)

    log_dir = Path.home() / "Saved Games" / "Frontier Developments" / "Elite Dangerous"
    watcher = JournalWatcher(log_dir, dispatcher)
    watcher.start()
    print("Журнал Elite Dangerous запущен! Для выхода нажмите Ctrl+C.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        watcher.stop()
        print("Завершено.")

if __name__ == "__main__":
    main()
