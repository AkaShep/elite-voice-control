import json
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from integration.journal.dispatcher import EventDispatcher
from .event_factory import parse_event

class JournalWatcher(FileSystemEventHandler):
    def __init__(self, log_dir: Path, dispatcher: EventDispatcher):
        self.log_dir = log_dir
        self.dispatcher = dispatcher
        self._positions = {}
        self._observer = Observer()

    def start(self):
        self._observer.schedule(self, str(self.log_dir), recursive=False)
        self._observer.start()
        self._read_existing_lines()

    def stop(self):
        self._observer.stop()
        self._observer.join()

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".log"):
            self._process_file(Path(event.src_path))

    def _read_existing_lines(self):
        for file in sorted(self.log_dir.glob("Journal*.log")):
            self._process_file(file, initial=True)

    def _process_file(self, file_path: Path, initial=False):
        position = self._positions.get(file_path, 0)
        with open(file_path, 'r', encoding='utf-8') as f:
            f.seek(position)
            lines = f.readlines()
            self._positions[file_path] = f.tell()

        for line in lines:
            try:
                data = json.loads(line)
                event = parse_event(data)
                if event:
                    self.dispatcher.dispatch(event)
            except Exception as e:
                print(f"[ERROR] Failed to process journal line: {e}")
