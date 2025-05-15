import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)
from core.tts_engine import TtsEngine

def test_tts():
    tts = TtsEngine()
    tts.synthesize("Привет! Я голосовой ассистент.")
    
if __name__ == "__main__":
    test_tts()