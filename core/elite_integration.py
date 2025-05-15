import os
import json
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class EliteStatusHandler:
    """Обработчик статуса корабля из Status.json"""
    def __init__(self):
        self.status = {}
        self.status_callbacks = []
        self.logger = logging.getLogger('EliteStatus')

    def add_callback(self, callback):
        """Добавление callback-функции для обновлений статуса"""
        self.status_callbacks.append(callback)

    def update(self, status_path: str):
        """Обновление статуса из файла"""
        try:
            with open(status_path, 'r') as f:
                new_status = json.load(f)
                if new_status != self.status:
                    self.status = new_status
                    self._trigger_callbacks()
        except Exception as e:
            self.logger.error(f"Status read error: {str(e)}")

    def _trigger_callbacks(self):
        """Вызов зарегистрированных callback-ов"""
        for callback in self.status_callbacks:
            callback(self.status)

class EliteJournalHandler(FileSystemEventHandler):
    """Обработчик журнальных событий"""
    def __init__(self, journal_callbacks=None):
        super().__init__()
        self.journal_callbacks = journal_callbacks or {}
        self.logger = logging.getLogger('EliteJournal')

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.log'):
            self._process_journal(event.src_path)

    def _process_journal(self, path: str):
        """Парсинг журнального файла"""
        try:
            with open(path, 'r') as f:
                for line in f:
                    event = json.loads(line)
                    self._handle_event(event)
        except Exception as e:
            self.logger.error(f"Journal read error: {str(e)}")

    def _handle_event(self, event: dict):
        """Вызов callback-ов для конкретного события"""
        event_type = event.get('event')
        if event_type in self.journal_callbacks:
            self.journal_callbacks[event_type](event)

class EliteIntegration:
    """Основной класс интеграции с Elite Dangerous"""
    def __init__(self):
        self.logger = logging.getLogger('EliteIntegration')
        self.observer = Observer()
        self.status_handler = EliteStatusHandler()
        self.journal_handler = EliteJournalHandler()
        self.log_path = self._get_default_log_path()

    @staticmethod
    def _get_default_log_path() -> Path:
        """Путь к папке с логами по умолчанию"""
        return Path.home() / 'Saved Games' / 'Frontier Developments' / 'Elite Dangerous'

    def start(self):
        """Запуск мониторинга логов"""
        if not self.log_path.exists():
            raise FileNotFoundError(f"Log directory not found: {self.log_path}")

        self.observer.schedule(
            self.journal_handler,
            path=str(self.log_path),
            recursive=False
        )
        self.observer.start()
        self.logger.info("Started log monitoring")

    def stop(self):
        """Остановка мониторинга"""
        self.observer.stop()
        self.observer.join()
        self.logger.info("Stopped log monitoring")

    def bind_status_update(self, callback):
        """Привязка обработчика обновлений статуса"""
        self.status_handler.add_callback(callback)

    def bind_journal_event(self, event_name: str, callback):
        """Привязка обработчика журнальных событий"""
        self.journal_handler.journal_callbacks[event_name] = callback

    def get_ship_status(self) -> dict:
        """Текущий статус корабля"""
        return self.status_handler.status

    @staticmethod
    def parse_ship_mode(flags: int) -> str:
        """Определение режима корабля по флагам"""
        modes = {
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
        }
        return next((mode for flag, mode in modes.items() if flags & flag), "Unknown")