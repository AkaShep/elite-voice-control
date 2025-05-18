import json
import logging
import os
from watchdog.events import FileSystemEventHandler

class EliteJournalHandler(FileSystemEventHandler):
    def __init__(self, journal_callbacks=None):
        super().__init__()
        self.journal_callbacks = journal_callbacks or {}
        self.logger = logging.getLogger('EliteJournal')
        self.file_positions = {}  # Для отслеживания позиций в файлах

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.log'):
            self._process_journal(event.src_path)

    def _process_journal(self, path: str):
        try:
            current_size = os.path.getsize(path)
            last_position = self.file_positions.get(path, 0)
            
            # Если файл уменьшился (пересоздан), читать с начала
            if current_size < last_position:
                last_position = 0
                
            with open(path, 'r') as f:
                f.seek(last_position)
                new_lines = f.readlines()
                self.file_positions[path] = f.tell()
                
                for line in new_lines:
                    self._handle_event(json.loads(line))
                    
        except Exception as e:
            self.logger.error(f"Journal error in {path}: {str(e)}", exc_info=True)

    def _handle_event(self, event: dict):
        event_type = event.get('event')
        if event_type in self.journal_callbacks:
            self.journal_callbacks[event_type](event)

class EventTypes:
    """Константы для типов событий"""
    LOCATION = "Location"
    CARGO = "Cargo"
    FUEL_SCOOP = "FuelScoop"
    UNDER_ATTACK = "UnderAttack"
    DANGER = "Danger"
    LOADOUT = "Loadout"
    SHIP_TARGETED = "ShipTargeted"
    FSD_JUMP = "FSDJump"