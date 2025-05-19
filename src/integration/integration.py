from pathlib import Path
from integration.journal.dispatcher import EventDispatcher
from integration.journal.watcher import JournalWatcher
from integration.events.location import LocationEvent
from integration.events.loadout import LoadoutEvent
from integration.events.cargo import CargoEvent
from integration.events.shiplocker import ShipLockerEvent

def print_location(event: LocationEvent):
    print(f"[LOCATION] System: {event.StarSystem}, Body: {event.Body}, Docked: {event.Docked}")

def print_loadout(event: LoadoutEvent):
    print(f"[LOADOUT] Ship: {event.Ship}, ShipName: {event.ShipName}")

def print_cargo(event: CargoEvent):
    print(f"[CARGO] Vessel: {event.Vessel}, Count: {event.Count}, Items: {event.Inventory}")

def print_shiplocker(event: ShipLockerEvent):
    print(f"[SHIPLOCKER] Consumables: {event.Consumables}")

def main():
    dispatcher = EventDispatcher()
    dispatcher.subscribe(LocationEvent, print_location)
    dispatcher.subscribe(LoadoutEvent, print_loadout)
    dispatcher.subscribe(CargoEvent, print_cargo)
    dispatcher.subscribe(ShipLockerEvent, print_shiplocker)

    log_dir = Path.home() / "Saved Games" / "Frontier Developments" / "Elite Dangerous"
    watcher = JournalWatcher(log_dir, dispatcher)
    watcher.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        watcher.stop()

if __name__ == "__main__":
    main()
