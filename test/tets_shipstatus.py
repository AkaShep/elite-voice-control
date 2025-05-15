# test_shipstatus.py
import os
import sys
import logging
import time
import json
from pathlib import Path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root_dir)
from core.elite_integration import EliteIntegration

def format_ship_status(status: dict) -> str:
    """Форматирование статуса корабля в читаемый вид"""
    try:
        # Получаем название модели корабля из разных источников
        ship_model = status.get('ShipType', status.get('ShipName', 'N/A'))
        
        # Для локализованных версий игры
        if isinstance(ship_model, dict):
            ship_model = ship_model.get('Localised', 'N/A')
            
        return (
            "\n=== КОРАБЕЛЬНЫЙ СТАТУС ==="
            f"\nМодель: {status.get('ShipType', 'N/A')}"
            f"\nТопливо: {status.get('Fuel', {}).get('FuelMain', 0):.1f} / "
            f"{status.get('Fuel', {}).get('FuelReservoir', 0):.1f}"
            f"\nРежим: {EliteIntegration.parse_ship_mode(status.get('Flags', 0))}"
            f"\nЗаряды: SYS[{status.get('Pips', [0]*3)[0]}] "
            f"ENG[{status.get('Pips', [0]*3)[1]}] "
            f"WEP[{status.get('Pips', [0]*3)[2]}]"
            f"\nГруз: {status.get('Cargo', 0)}T | "
            f"Целостность: {status.get('Hull', 100.0)}%"
            "\n==========================="
        )
    except KeyError as e:
        logging.error(f"Ошибка форматера: отсутствует ключ {str(e)}")
        return ""

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )
    
    integrator = EliteIntegration()
    status_file = integrator.log_path / "Status.json"
    
    try:
        logging.info("Запуск периодической проверки статуса (интервал 5 сек)")
        while True:
            if status_file.exists():
                try:
                    with open(status_file, 'r') as f:
                        status = json.load(f)
                        print(format_ship_status(status))
                except json.JSONDecodeError:
                    logging.warning("Ошибка чтения файла статуса: невалидный JSON")
                except Exception as e:
                    logging.error(f"Ошибка чтения статуса: {str(e)}")
            else:
                logging.warning("Файл статуса не найден")
            
            time.sleep(5)
            
    except KeyboardInterrupt:
        logging.info("Остановка мониторинга...")
        sys.exit(0)

if __name__ == "__main__":
    main()