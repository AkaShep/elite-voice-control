# test/test_echo.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.settings import SAMPLE_RATE, DEVICE

from core.speech_recognition import SpeechRecognizer
from core.tts_engine import TtsEngine
from core.elite_integration import EliteIntegration
import sounddevice as sd
import queue
import numpy as np

class VoiceEcho:

    def __init__(self):
        self.elite = EliteIntegration()
        self.tts = TtsEngine()

    def __init__(self):
        self.recognizer = SpeechRecognizer()
        self.tts = TtsEngine()
        self.audio_queue = queue.Queue()
        self.sample_rate = SAMPLE_RATE  # Должно совпадать с настройками Vosk

    def _audio_callback(self, indata, frames, time, status):
        """Запись аудио в реальном времени"""
        self.audio_queue.put(indata.copy())

    def run(self):
        """Основной цикл: слушаем → распознаем → синтезируем"""
        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            device=DEVICE,
            dtype=np.int16,
            callback=self._audio_callback
        ):
            print("Скажите что-нибудь... (Ctrl+C для выхода)")
            while True:
                try:
                    # Запись аудио (2 секунды для примера)
                    audio_data = np.concatenate([self.audio_queue.get() for _ in range(4)])
                    audio_bytes = audio_data.tobytes()

                    # Распознавание
                    text = self.recognizer.recognize(audio_bytes)
                    if text:
                        print(f"Распознано: {text}")
                        
                        # Синтез и воспроизведение
                        self.tts.synthesize(text)
                        
                except KeyboardInterrupt:
                    print("\nЗавершение работы")
                    break

if __name__ == "__main__":
    echo = VoiceEcho()
    echo.run()
    