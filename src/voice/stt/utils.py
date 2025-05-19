import numpy as np

def is_silence(audio_bytes, threshold=400):
    """Проверяет, является ли аудиоблок тишиной (по амплитуде)"""
    arr = np.frombuffer(audio_bytes, dtype=np.int16)
    return np.abs(arr).mean() < threshold

def normalize_text(text):
    """Простейшая коррекция часто ошибочных слов"""
    corrections = {
        "стыковку": "стыковка",
        "стиковка": "стыковка",
        "галактика": "карта галактики"
        # ...добавь по опыту работы с распознаванием
    }
    text = text.strip().lower()
    return corrections.get(text, text)
