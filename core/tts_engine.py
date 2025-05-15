import os
import torch
import time
import numpy as np
import sounddevice as sd
from pathlib import Path
from config.settings import SILERO_MODEL_PATH, TTS_SAMPLE_RATE, TTS_SETTINGS, TTS_DEVICE
from functools import lru_cache
from symspellpy import SymSpell  # Импорт библиотеки для исправления опечаток
from num2words import num2words
import re
import logging
from typing import Optional

class TtsEngine:
    def __init__(self):
        self._check_model()
        self.model, self.speaker = self._load_model()
        self.sample_rate = TTS_SAMPLE_RATE
        self.device = torch.device(TTS_DEVICE)
        self._init_spell_checker()  # Инициализация проверки орфографии
        self._warm_up()

    def _init_spell_checker(self):
        """Инициализация корректора опечаток"""
        self.sym_spell = SymSpell()
        dictionary_path = os.path.join(os.path.dirname(__file__), "..", "config", "ru_elite_dangerous.txt")
        self.sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

    def _check_model(self):
        """Проверка наличия модели Silero"""
        if not Path(SILERO_MODEL_PATH).exists():
            raise FileNotFoundError(f"Модель Silero не найдена: {SILERO_MODEL_PATH}")

    def _load_model(self):
        """Загрузка модели"""
        model = torch.package.PackageImporter(SILERO_MODEL_PATH).load_pickle("tts_models", "model")
        return model, TTS_SETTINGS['speaker']

    def _warm_up(self):
        """Прогрев модели при запуске"""
        self.model.apply_tts(text="тест синтеза речи", speaker=self.speaker, sample_rate=self.sample_rate)

    def _convert_numbers_to_words(self, text: str) -> str:
        """Конвертация всех чисел в тексте в слова с правильным склонением"""
        def replace_number(match):
            number = float(match.group())
            try:
                if number.is_integer():
                    return num2words(int(number), lang='ru', gender='f')
                integer_part = int(number)
                fractional = round(number - integer_part, 1)
                return (
                    f"{num2words(integer_part, lang='ru')} "
                    f"целых {num2words(int(fractional*10), lang='ru')} десятых"
                )
            except Exception as e:
                logging.error(f"Ошибка конвертации числа: {str(e)}")
                return match.group()

        return re.sub(r'\b\d+\.?\d*\b', replace_number, text)

    def _decline_tonnage(self, text: str) -> str:
        """Склонение слова 'тонн' в зависимости от числительного"""
        def replace_tonnage(match):
            number = float(match.group(1))
            try:
                if 11 <= (number % 100) <= 14:
                    return f"{match.group(1)} тонн"
                last_digit = int(number) % 10
                if last_digit == 1:
                    return f"{match.group(1)} тонна"
                elif 2 <= last_digit <= 4:
                    return f"{match.group(1)} тонны"
                return f"{match.group(1)} тонн"
            except Exception as e:
                logging.error(f"Ошибка склонения: {str(e)}")
                return match.group(0)

        return re.sub(r'(\d+\.?\d*)\s+тонн', replace_tonnage, text)

    @lru_cache(maxsize=100)
    def synthesize(self, text: str) -> None:
        """Синтез речи из текста с проверкой опечаток"""
        if not text.strip():
            return  # Пропустить пустой текст
        
        # Исправление опечаток
        corrected_text = self._correct_text(text)
        if not corrected_text:
            return

        start_time = time.time()
        try:
            # 1. Предобработка текста
            processed_text = self._convert_numbers_to_words(text)
            processed_text = self._decline_tonnage(processed_text)
            
            # 2. Исправление опечаток
            corrected_text = self._correct_text(processed_text)
            # 3. Синтез речи
            audio = self.model.apply_tts(
                text=corrected_text,
                speaker=self.speaker,
                sample_rate=self.sample_rate,
                **TTS_SETTINGS['params']
            )
            print(f"Синтез занял: {time.time() - start_time:.2f} сек")
            self._play_audio(audio.numpy())
        except Exception as e:
            raise RuntimeError(f"Ошибка синтеза речи: {str(e)}")

    def _correct_text(self, text: str) -> str:
        """Коррекция опечаток"""
        suggestions = self.sym_spell.lookup(text, verbosity=2)
        return suggestions[0].term if suggestions else text

    def _play_audio(self, audio: np.ndarray):
        """Воспроизведение аудио через sounddevice"""
        sd.play(audio, self.sample_rate)
        sd.wait()