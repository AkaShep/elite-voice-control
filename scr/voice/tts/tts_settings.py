import os
from pathlib import Path

SILERO_MODEL_PATH = os.path.join(Path(__file__).parent, "model/model.pt")
TTS_SAMPLE_RATE = 48000
TTS_DEVICE = "cpu"  # cpu или cuda(GPU)
TTS_SETTINGS = {
    'speaker': 'kseniya',  # Варианты: aidar, baya, kseniya, xenia, random
    'params': {
        'put_accent': True,
        'put_yo': True,
    }
}