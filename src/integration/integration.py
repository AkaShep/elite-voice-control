from pathlib import Path
from integration.journal.dispatcher import EventDispatcher
from integration.journal.watcher import JournalWatcher
from integration.journal.event_factory import parse_event

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
