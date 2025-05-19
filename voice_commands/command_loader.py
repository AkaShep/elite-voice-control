import yaml
import os
from typing import Dict

class CommandLoader:
    def __init__(self, directory: str):
        self.directory = directory
        self.commands: Dict[str, str] = {}

    def load(self):
        """Загружает все YAML-файлы с командами из указанной директории."""
        for filename in os.listdir(self.directory):
            if filename.endswith('.yaml'):
                full_path = os.path.join(self.directory, filename)
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                        if isinstance(data, dict):
                            self.commands.update(data)
                except Exception as e:
                    print(f"Ошибка загрузки файла {filename}: {str(e)}")

    def get_all_commands(self) -> Dict[str, str]:
        return self.commands