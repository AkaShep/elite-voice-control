from src.voice.tts.tts_engine import TtsEngine

def test_tts():
    tts = TtsEngine()
    tts.synthesize("Привет! Я голосовой ассистент.")
    
if __name__ == "__main__":
    test_tts()