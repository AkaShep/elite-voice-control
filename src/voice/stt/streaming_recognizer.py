import sounddevice as sd
import queue
import threading
import json
from vosk import Model, KaldiRecognizer
from .stt_settings import MODEL_VOSK_PATH, SAMPLE_RATE, DEVICE
from .utils import is_silence, normalize_text

class StreamingSpeechRecognizer:
    """
    Класс потокового распознавания речи на базе Vosk.
    Поддерживает wake word, динамическую грамматику, автостоп по тишине,
    асинхронность и логирование.
    """
    def __init__(
        self,
        wake_word="компьютер",
        commands=None,
        log_file="stt_log.txt",
        silence_threshold=400,
        max_silence_blocks=5
    ):
        self.model = Model(MODEL_VOSK_PATH)
        self.sample_rate = SAMPLE_RATE
        self.device = DEVICE
        self.wake_word = wake_word.lower() if wake_word else None
        self.commands = commands if commands else []
        self.log_file = log_file
        self.silence_threshold = silence_threshold
        self.max_silence_blocks = max_silence_blocks
        self.running = False
        self.q = queue.Queue()

        # Инициализация распознавателя с динамической грамматикой (если нужна)
        if self.commands:
            grammar = json.dumps(self.commands)
            self.rec = KaldiRecognizer(self.model, self.sample_rate, grammar)
        else:
            self.rec = KaldiRecognizer(self.model, self.sample_rate)

    def _audio_callback(self, indata, frames, time, status):
        """Callback для sounddevice — отправляет аудиоданные в очередь"""
        self.q.put(bytes(indata))

    def _log_unrecognized(self, text):
        """Логирование нераспознанных или неактуальных фраз"""
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(text + "\n")

    def recognize_stream(self, on_command):
        """
        Основной цикл потокового распознавания. Вызывает on_command(текст) для команд.
        """
        self.running = True
        silence_blocks = 0
        speech_started = False

        print("Скажите активационное слово для начала (или команду, если wake word не требуется)...")
        with sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=8000,
            dtype='int16',
            channels=1,
            device=self.device,
            callback=self._audio_callback
        ):
            while self.running:
                data = self.q.get()
                if is_silence(data, self.silence_threshold):
                    if speech_started:
                        silence_blocks += 1
                        if silence_blocks >= self.max_silence_blocks:
                            print("Конец речи.")
                            speech_started = False
                            silence_blocks = 0
                    continue
                else:
                    silence_blocks = 0
                    speech_started = True

                # Потоковое распознавание
                if self.rec.AcceptWaveform(data):
                    result = json.loads(self.rec.Result())
                    text = result.get("text", "").strip()
                    if text:
                        print(f"[Vosk] Результат: '{text}'")
                        text = normalize_text(text)

                        # Wake word логика
                        if self.wake_word:
                            if text == self.wake_word:
                                print("Активационное слово распознано! Говорите команду...")
                                temp = self.wake_word
                                self.wake_word = None
                                self.recognize_stream(on_command)
                                self.wake_word = temp
                                break
                            else:
                                self._log_unrecognized(text)
                        else:
                            # Реакция на команду после активации
                            if self.commands and text not in self.commands:
                                print(f"Неизвестная команда: '{text}'")
                                self._log_unrecognized(text)
                            else:
                                on_command(text)
                    else:
                        print("[Vosk] Пустой результат")
                else:
                    partial = json.loads(self.rec.PartialResult())
                    partial_text = partial.get("partial", "")
                    # print(f"[Partial] {partial_text}")

    def run_in_thread(self, on_command):
        """
        Запускает потоковое распознавание в отдельном потоке.
        """
        thread = threading.Thread(target=self.recognize_stream, args=(on_command,), daemon=True)
        thread.start()
        return thread

    def stop(self):
        """Остановить поток распознавания."""
        self.running = False

# ===== Пример использования =====
if __name__ == "__main__":
    def handle_command(cmd):
        print(f"РАСПОЗНАНА КОМАНДА: {cmd}")
        if cmd == "выход":
            print("Ассистент завершает работу.")
            rec.stop()
    commands = ["стыковка", "карта галактики", "прыжок", "выход"]
    rec = StreamingSpeechRecognizer(
        wake_word="компьютер",
        commands=commands
    )
    rec.run_in_thread(handle_command)

    import time
    try:
        while rec.running:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nОстановка ассистента.")
        rec.stop()
