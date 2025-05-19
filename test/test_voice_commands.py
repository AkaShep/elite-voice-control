import logging
from src import SpeechRecognizer
from src import TtsEngine
from voice_commands.command_loader import CommandLoader
from voice_commands import VoiceCommandProcessor

def main():
    logging.basicConfig(level=logging.INFO)

    # Загрузка команд
    loader = CommandLoader("voice_commands/categories")
    loader.load()
    commands = loader.get_all_commands()

    # Инициализация
    tts = TtsEngine()
    recognizer = SpeechRecognizer()
    processor = VoiceCommandProcessor(tts, commands)

    print("Говорите команду (Ctrl+C для выхода)...")

    import sounddevice as sd
    import numpy as np

    duration = 3  # секунды

    try:
        while True:
            print("🎤 Запись...")
            audio = sd.rec(int(duration * 16000), samplerate=16000, channels=1, dtype='int16')
            sd.wait()
            audio_bytes = audio.tobytes()

            text = recognizer.recognize(audio_bytes)
            print(f"Вы сказали: {text}")

            if not processor.handle_command(text):
                tts.synthesize("Команда не распознана.")
    except KeyboardInterrupt:
        print("🛑 Завершено.")

if __name__ == "__main__":
    main()
