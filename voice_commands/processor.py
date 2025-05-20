import logging
from typing import Dict, Optional
from difflib import get_close_matches
from src.integration.api.api_interpreter import interpret_and_execute

class VoiceCommandProcessor:
    def __init__(self, tts_engine, command_dict: Dict[str, str]):
        self.tts = tts_engine
        self.commands = command_dict
        self.logger = logging.getLogger('VoiceCommands')
        self.similarity_threshold = 0.8

    def handle_command(self, phrase: str) -> bool:
        """
        Обрабатывает фразу. Если команда найдена в словаре или по близости,
        выполняет API и озвучивает через TTS. Возвращает True, если команда распознана.
        """
        normalized = phrase.lower().strip()
        response = self.commands.get(normalized)

        if response:
            self._respond(normalized, response)
            return True

        close_matches = get_close_matches(normalized, self.commands.keys(), n=1, cutoff=self.similarity_threshold)
        if close_matches:
            match = close_matches[0]
            response = self.commands[match]
            self._respond(match, response, original=normalized)
            return True

        self.logger.warning(f"Команда не распознана: '{normalized}'")
        return False

    def _respond(self, command: str, response: str, original: Optional[str] = None):
        if original and original != command:
            self.logger.info(f"Похожая команда: '{original}' → '{command}' → '{response}'")
        else:
            self.logger.info(f"Команда: '{command}' → '{response}'")

        cleaned = interpret_and_execute(response)
        if cleaned:
            self.tts.synthesize(cleaned)
