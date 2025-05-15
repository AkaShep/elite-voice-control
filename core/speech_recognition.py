from vosk import Model, KaldiRecognizer
import json
import os
from pathlib import Path  # Добавлен импорт
from config.settings import MODEL_VOSK_PATH, SAMPLE_RATE

class SpeechRecognizer:
    def __init__(self):
        """Инициализация модели Vosk."""
        self._check_model()  # Вызов метода проверки
        self.model = Model(MODEL_VOSK_PATH)
        self.recognizer = KaldiRecognizer(self.model, SAMPLE_RATE)

    def _check_model(self):
        """Проверка наличия модели Vosk"""
        if not Path(MODEL_VOSK_PATH).exists():
            raise FileNotFoundError(f"Модель не найдена: {MODEL_VOSK_PATH}")

    def recognize(self, audio_data: bytes) -> str:
        """Распознавание речи из аудиоданных в формате bytes."""
        if self.recognizer.AcceptWaveform(audio_data):
            result = json.loads(self.recognizer.Result())
            return result.get("text", "")
        return ""