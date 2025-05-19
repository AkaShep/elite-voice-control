 # основной интегратор
from pathlib import Path
from .journal.dispatcher import EventDispatcher
from .journal.watcher import JournalWatcher
from .state.ship_state import ShipState
from .events.fsd_jump import FSDJumpEvent

class EliteIntegration:
    def __init__(self):
        self.dispatcher = EventDispatcher()
        self.ship_state = ShipState()

        self._bind_subscribers()

        self.watcher = JournalWatcher(self.get_log_dir(), self.dispatcher)

    def _bind_subscribers(self):
        self.dispatcher.subscribe(FSDJumpEvent, self.ship_state.on_fsd_jump)

    def start(self):
        self.watcher.start()

    def stop(self):
        self.watcher.stop()

    @staticmethod
    def get_log_dir() -> Path:
        return Path.home() / "Saved Games" / "Frontier Developments" / "Elite Dangerous"
