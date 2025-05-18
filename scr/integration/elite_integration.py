import json
import logging
from pathlib import Path
from threading import Timer, Lock
from watchdog.observers import Observer
from .ship_state import ShipState
from .events import EliteJournalHandler, EventTypes

class EliteStatusHandler:
    """Обработчик статуса корабля из Status.json"""
    def __init__(self):
        self.status = {}
        self.status_callbacks = []
        self.logger = logging.getLogger('EliteStatus')

    def add_callback(self, callback):
        self.status_callbacks.append(callback)

    def update(self, status_path: str):
        try:
            with open(status_path, 'r') as f:
                new_status = json.load(f)
                if new_status != self.status:
                    self.status = new_status
                    self._trigger_callbacks()
                    self.logger.debug("Status updated: %s", self.status)
        except Exception as e:
            self.logger.error(f"Status read error: {str(e)}")

    def _trigger_callbacks(self):
        for callback in self.status_callbacks:
            callback(self.status)

class EliteIntegration:
    """Основной класс интеграции"""
    def __init__(self):
        self.logger = logging.getLogger('EliteIntegration')
        self.observer = Observer()
        self.journal_handler = EliteJournalHandler()
        self.ship_state = ShipState()
        self.log_path = self._get_default_log_path()
        self.status_file = self.log_path / "Status.json"
        self._timer = None
        self._timer_lock = Lock()
        
        self._bind_handlers()

    def _bind_handlers(self):
        # Журнальные события
        self.journal_handler.journal_callbacks = {
            EventTypes.LOADOUT: self.ship_state.update_from_journal_event,
            EventTypes.CARGO: self.ship_state.update_from_journal_event,
            EventTypes.LOCATION: self._handle_location_event,
            EventTypes.FUEL_SCOOP: self.ship_state.update_from_journal_event,
            EventTypes.UNDER_ATTACK: self.ship_state.update_from_journal_event,
            EventTypes.SHIP_TARGETED: self._handle_target_event,
            EventTypes.FSD_JUMP: self._handle_fsd_jump,            
        }
        # Периодические обновления статуса
        self._start_periodic_updates()   

    def _handle_target_event(self, event: dict):
        target = event.get("TargetLocked", False)
        self.ship_state.target_locked = target 

    def _handle_fsd_jump(self, event: dict):
        if "StarSystem" in event:
            self.ship_state.current_system = event["StarSystem"]
        self.ship_state.update_from_journal_event(event) 

    def _handle_location_event(self, event: dict):
        if "StarSystem" in event:
            self.ship_state.current_system = event["StarSystem"]
        self.ship_state.update_from_journal_event(event)     

    def _start_periodic_updates(self):
        def status_check():
            with self._timer_lock:
                if self.status_file.exists():
                    try:
                        with open(self.status_file, 'r') as f:
                            status = json.load(f)
                            self.ship_state.update_from_status(status)
                    except Exception as e:
                        self.logger.error(f"Status read error: {str(e)}", exc_info=True)
                
                self._timer = Timer(1.0, status_check)
                self._timer.start()
        
        status_check()

    def _handle_status_update(self, status: dict):
        self.ship_state.update_from_status(status)

    def _handle_journal_event(self, event: dict):
        self.ship_state.update_from_journal_event(event)

    @staticmethod
    def _get_default_log_path() -> Path:
        return Path.home() / 'Saved Games' / 'Frontier Developments' / 'Elite Dangerous'

    def start(self):
        if not self.log_path.exists():
            raise FileNotFoundError(f"Log directory not found: {self.log_path}")
        
        self.observer.schedule(
            self.journal_handler,
            path=str(self.log_path),
            recursive=False
        )
        self.observer.start()
        self.logger.info("Monitoring started")

    def stop(self):
        with self._timer_lock:
            if self._timer:
                self._timer.cancel()
        self.observer.stop()
        self.observer.join()
        self.logger.info("Monitoring stopped")



    @staticmethod
    def parse_ship_mode(flags: int) -> str:
        """Определение режима корабля по флагам"""
        modes = []
        for flag, mode in {
            1 << 0: "Docked",
            1 << 1: "Landed",
            1 << 2: "LandingGear",
            1 << 3: "Shields",
            1 << 4: "Supercruise",
            1 << 5: "FlightAssist",
            1 << 6: "Hardpoints",
            1 << 7: "Winging",
            1 << 8: "Lights",
            1 << 9: "CargoScoop",
            1 << 10: "SilentRunning",
            1 << 11: "Scooping",
            1 << 12: "SRVHandbrake",
            1 << 13: "SRVTurret",
            1 << 14: "SRVUnderShip",
            1 << 15: "SRVDriveAssist",
            1 << 16: "FSDMassLocked",
            1 << 17: "FSDCharging",
            1 << 18: "FSDCooldown",
            1 << 19: "LowFuel",
            1 << 20: "Overheating",
            1 << 21: "HasLatLong",
            1 << 22: "InDanger",
            1 << 23: "InInterdiction",
            1 << 24: "InMothership",
            1 << 25: "InFighter",
            1 << 26: "InSRV",
            1 << 27: "AnalysisMode",
            1 << 28: "NightVision"
        }.items():
            if flags & flag:
                modes.append(mode)
        return ", ".join(modes) if modes else "Unknown"
       