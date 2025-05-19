# src/integration/mode_manager.py Управление режимами STT

from voice.stt.streaming_recognizer import StreamingSpeechRecognizer

class AssistantModeManager:
    """
    Переключает STT между 'routine' (wake word) и 'combat' (always on)
    """
    def __init__(self, context, tts, handle_routine, handle_combat):
        self.context = context
        self.tts = tts
        self.handle_routine = handle_routine
        self.handle_combat = handle_combat
        self.current_stt = None

    def start_routine_mode(self):
        self.context.assistant_mode = "routine"
        print("[Ассистент] Включен обычный режим. Активация по слову 'Гидеон'.")
        self.tts.synthesize("Режим обычных команд активирован.")
        self._stop_current_stt()
        self.current_stt = StreamingSpeechRecognizer(
            wake_word="гидеон",
            commands=[
                "открой карту", "заправься", "включи дальномер", "показать задание",
                "выход", "боевой режим"
            ]
        )
        self.current_stt.run_in_thread(self.handle_routine)

    def start_combat_mode(self):
        self.context.assistant_mode = "combat"
        print("[Ассистент] Боевое прослушивание. Голосовые команды без активации.")
        self.tts.synthesize("Боевое голосовое управление включено.")
        self._stop_current_stt()
        self.current_stt = StreamingSpeechRecognizer(
            wake_word=None,
            commands=[
                "ракеты", "щит", "отступить", "огонь", "перезарядка", "уход",
                "выход из боя"
            ]
        )
        self.current_stt.run_in_thread(self.handle_combat)

    def _stop_current_stt(self):
        if self.current_stt is not None:
            self.current_stt.stop()
            self.current_stt = None
