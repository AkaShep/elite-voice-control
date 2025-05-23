import sys
import os
import json
import queue
import numpy as np
import sounddevice as sd

# Фиксируем путь к корневой директории проекта
#from src.voice.stt.speech_recognition import SpeechRecognizer
#from src.voice.stt.stt_settings import SAMPLE_RATE, DEVICE
from src import SpeechRecognizer, SAMPLE_RATE, DEVICE

class RealTimeRecognizer:
    def __init__(self):
        self.sample_rate = SAMPLE_RATE
        self.audio_queue = queue.Queue()
        self.recognizer = SpeechRecognizer()

    def _audio_callback(self, indata, frames, time, status):
        """Callback для записи аудиопотока"""
        self.audio_queue.put(indata.tobytes())

    def start(self):
        """Запуск непрерывного распознавания"""
        with sd.InputStream(
            samplerate=self.sample_rate,
            device=DEVICE,
            channels=1,
            dtype=np.int16,
            callback=self._audio_callback
        ):
            print("Слушаю... (Нажмите Ctrl+C для остановки)")
            while True:
                try:
                    audio_bytes = self.audio_queue.get()
                    text = self.recognizer.recognize(audio_bytes)
                    
                    # Вывод результатов
                    if text:
                        print("\nРаспознано:", text)
                    else:
                        partial = json.loads(self.recognizer.recognizer.PartialResult())
                        if partial.get("partial", ""):
                            print(f"\rЧастичный результат: {partial['partial']}", end="", flush=True)
                except KeyboardInterrupt:
                    print("\nОстановка распознавания")
                    break

if __name__ == "__main__":
    try:
        rt_recognizer = RealTimeRecognizer()
        rt_recognizer.start()
    except Exception as e:
        print(f"Ошибка: {str(e)}")