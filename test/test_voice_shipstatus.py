# test_voice_shipstatus.py
import os
import sys
import json
import logging
import re
from num2words import num2words
from pathlib import Path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root_dir)
from core.elite_integration import EliteIntegration
from core.tts_engine import TtsEngine

class VoiceShipStatusReporter:
    """Класс для голосового отчета о статусе корабля с улучшенным произношением"""
    
    def __init__(self):
        self.integrator = EliteIntegration()
        self.tts = TtsEngine()
        self.logger = logging.getLogger('VoiceShipStatus')
        self.status_file = self.integrator.log_path / "Status.json"

    def _get_ship_status(self) -> dict:
        """Получение текущего статуса корабля с обработкой ошибок"""
        try:
            if not self.status_file.exists():
                self.logger.warning("Файл статуса не найден")
                return {}
                
            with open(self.status_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Ошибка чтения статуса: {str(e)}")
            return {}        

    def _format_for_speech(self, status: dict) -> str:
        """Генерация естественно звучащего отчета"""
        try:
            # Определение модели корабля
            ship_model = status.get('ShipType', status.get('ShipName', 'неизвестный корабль'))
            if isinstance(ship_model, dict):
                ship_model = ship_model.get('Localised', 'неизвестный корабль')

            # Форматирование числовых значений
            fuel_main = self._format_number(status.get('Fuel', {}).get('FuelMain', 0))
            fuel_reservoir = self._format_number(status.get('Fuel', {}).get('FuelReservoir', 0))
            hull = self._format_number(status.get('Hull', 100))
            cargo_value = status.get('Cargo', 0)
            cargo_words = self._format_number(cargo_value)

            """Упрощенное форматирование для передачи в TTS"""
            return (
                f"Статус: {status.get('ShipName', 'корабль')}. "
                f"Топливо: {status.get('Fuel', {}).get('FuelMain', 0)}. "
                f"Резерв: {status.get('Fuel', {}).get('FuelReservoir', 0)}. "
                f"Корпус: {status.get('Hull', 100)}%. "
                f"Груз: {status.get('Cargo', 0)} тонн."
            )
            
        except Exception as e:
            self.logger.error(f"Ошибка форматирования: {str(e)}")
            return "Не удалось получить информацию о состоянии корабля"

    def report_status(self):
        """Полный цикл формирования и озвучки отчета"""
        status = self._get_ship_status()
        if not status:
            self.logger.error("Нет данных для отчета")
            return
            
        speech_text = self._format_for_speech(status)
        self.logger.info("Формирование отчета...")
        
        try:
            print("\nСгенерированный текст:", speech_text)
            self.tts.synthesize(speech_text)
            self.logger.info("Озвучка выполнена успешно")
        except Exception as e:
            self.logger.error(f"Ошибка синтеза речи: {str(e)}")

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )
    
    reporter = VoiceShipStatusReporter()
    reporter.report_status()

if __name__ == "__main__":
    main()