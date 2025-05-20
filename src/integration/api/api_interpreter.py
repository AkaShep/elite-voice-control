import re
import logging
from integration.api.elite_api import EliteAPI

logger = logging.getLogger(__name__)

COMMAND_PATTERN = re.compile(r"\(\(EliteAPI\.([A-Za-z0-9_]+)\)\)")

def interpret_and_execute(text: str) -> str:
    """
    Распознаёт API-команды в тексте и выполняет их.
    Возвращает текст без команд, пригодный для TTS.
    """
    matches = COMMAND_PATTERN.findall(text)
    for command in matches:
        logger.info(f"Обнаружена команда EliteAPI: {command}")
        EliteAPI.execute(command)

    return COMMAND_PATTERN.sub("", text).strip()
