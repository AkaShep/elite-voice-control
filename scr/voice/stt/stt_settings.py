from pathlib import Path
import os
MODEL_VOSK_PATH = os.path.join(Path(__file__).parent, "model")

SAMPLE_RATE = 16000        # Частота записи с микрофона (Гц)
DEFAULT_DURATION = 5      # Длительность записи по умолчанию (сек)
DEVICE = None     # ID аудиоустройства (None = система по умолчанию)