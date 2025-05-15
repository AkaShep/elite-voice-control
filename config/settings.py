from pathlib import Path
import os

# Пути к моделям
MODEL_VOSK_PATH = os.path.join(Path(__file__).parent.parent, "models/vosk")
MODEL_SILERO_PATH = os.path.join(Path(__file__).parent.parent, "models/silero")
OUTPUT_DIR = os.path.join(Path(__file__).parent.parent, "outputs")
SILERO_MODEL_PATH = os.path.join(MODEL_SILERO_PATH, "model.pt")  # Исправлен путь

# Настройки аудио
TTS_SAMPLE_RATE = 48000
SAMPLE_RATE = 16000        # Частота записи с микрофона (Гц)
DEFAULT_DURATION = 5      # Длительность записи по умолчанию (сек)
DEVICE = None     # ID аудиоустройства (None = система по умолчанию)

# Настройки TTS
TTS_DEVICE = "cpu"  # cpu или cuda(GPU)
TTS_SETTINGS = {
    'speaker': 'kseniya',  # Варианты: aidar, baya, kseniya, xenia, random
    'params': {
        'put_accent': True,
        'put_yo': True,
    }
}

KEY_BINDINGS = {
    "engines": "e",
    "map": ["shift", "tab"],
    "full_stop": "x"
}