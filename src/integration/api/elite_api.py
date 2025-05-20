import logging
import keyboard
import ctypes
import time

logger = logging.getLogger(__name__)

class EliteAPI:
    """
    API-обёртка для взаимодействия с игрой Elite Dangerous через эмуляцию клавиш.
    Использует библиотеку 'keyboard' для надёжной работы вне зависимости от раскладки.
    """

    @staticmethod
    def _check_layout():
        user32 = ctypes.WinDLL('user32', use_last_error=True)
        layout = user32.GetKeyboardLayout(0)
        if (layout & 0xFFFF) != 0x409:
            logger.warning("Внимание: включена не английская раскладка. Рекомендуется переключить на EN для корректной работы команд.")

    @staticmethod
    def deployLandingGear():
        EliteAPI._check_layout()
        logger.info("Выпуск шасси (нажатие клавиши 'L')")
        keyboard.press_and_release('l')

    @staticmethod
    def toggleLights():
        EliteAPI._check_layout()
        logger.info("Переключение освещения (нажатие клавиши 'Insert')")
        keyboard.press_and_release('insert')

    @staticmethod
    def launchFighter():
        EliteAPI._check_layout()
        logger.info("Запуск истребителя через панель экипажа")
        keyboard.press_and_release('5')
        time.sleep(1)
        keyboard.press_and_release('down')
        keyboard.press_and_release('enter')

    @staticmethod
    def silentRunning():
        EliteAPI._check_layout()
        logger.info("Активация бесшумного режима (нажатие клавиши 'DELETE')")
        keyboard.press_and_release('delete')

    @staticmethod
    def rebootRepair():
        EliteAPI._check_layout()
        logger.info("Перезапуск и ремонт (горячая клавиша Ctrl+R)")
        keyboard.send('ctrl+r')

    @staticmethod
    def execute(command: str, *args):
        method_name = command[0].lower() + command[1:]
        method = getattr(EliteAPI, method_name, None)
        if callable(method):
            logger.debug(f"Выполнение API-команды: {command} с аргументами {args}")
            return method(*args)
        else:
            logger.warning(f"Неизвестная команда EliteAPI: {command}")
            return None
