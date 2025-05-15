import pyautogui
from config.settings import KEY_BINDINGS  # Добавьте настройки клавиш в config

class GameController:
    def __init__(self):
        self.commands = {
            "запустить двигатели": self._activate_engines,
            "открыть карту": self._open_map,
            "полный стоп": self._full_stop,
        }

    def execute_command(self, command: str) -> bool:
        """Выполнить действие по голосовой команде."""
        action = self.commands.get(command.strip().lower())
        if action:
            action()
            return True
        return False

    def _activate_engines(self):
        pyautogui.press(KEY_BINDINGS["engines"])  # Пример: клавиша 'E'

    def _open_map(self):
        pyautogui.hotkey("shift", "tab")  # Комбинация для карты

    def _full_stop(self):
        pyautogui.keyDown("x")
        time.sleep(1)
        pyautogui.keyUp("x")