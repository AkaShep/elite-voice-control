import logging
from typing import Dict

class VoiceCommandProcessor:
    def __init__(self, tts_engine, command_dict: Dict[str, str]):
        self.tts = tts_engine
        self.commands = command_dict
        self.logger = logging.getLogger('VoiceCommands')

    def handle_command(self, phrase: str) -> bool:
        """
        Обрабатывает фразу. Если команда найдена в словаре,
        озвучивает её через TTS.
        Возвращает True, если команда распознана.
        """
        normalized = phrase.lower().strip()
        response = self.commands.get(normalized)

        if response:
            self.logger.info(f"Команда: '{normalized}' → Ответ: '{response}'")
            self.tts.synthesize(response)
            return True
        else:
            self.logger.info(f"Команда не распознана: '{normalized}'")
            return False
