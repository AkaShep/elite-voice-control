# test_voice_shipstatus.py
import logging
from scr import EliteIntegration
from scr import ShipState  # Импорт нового класса состояния

class VoiceShipStatusReporter:
    """Класс для голосового отчета о статусе корабля"""
    
    def __init__(self):
        self.integrator = EliteIntegration()
        self.integrator.start()  # Запускаем мониторинг
        self.tts = self._init_tts()  
        self.logger = logging.getLogger('VoiceShipStatus')

    def _init_tts(self):
        # Убедитесь, что модуль TtsEngine доступен
        from scr import TtsEngine  # Или укажите правильный путь
        return TtsEngine()

    def _format_for_speech(self) -> str:
        """Генерация отчета из ShipState"""
        state = self.integrator.ship_state
        
        return (
            f"Статус: {state.ship_name or 'корабль'}. "
            f"Топливо: {state.fuel:.1f} тонн. "
            f"Резерв: {state.fuel_level:.1f} тонн. "
            f"Корпус: {state.health:.0f}%. "
            f"Груз: {state.total_cargo} тонн. "
            f"Режим: {self._get_ship_mode()}"
        )

    def _get_ship_mode(self) -> str:
        """Получение режима корабля через интегратор"""
        flags = self.integrator.status_handler.status.get('Flags', 0)
        return EliteIntegration.parse_ship_mode(flags)

    def report_status(self):
        """Формирование и озвучка отчета"""
        try:
            speech_text = self._format_for_speech()
            self.logger.info("Формирование отчета...\n%s", speech_text)
            self.tts.synthesize(speech_text)
        except Exception as e:
            self.logger.error(f"Ошибка: {str(e)}")

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