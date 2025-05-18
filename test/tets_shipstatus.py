import logging
import time
from scr import EliteIntegration

def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )
    
    integrator = EliteIntegration()
    integrator.start()
    
    try:
        while True:
            state = integrator.ship_state
            flags = integrator.status_handler.status.get("Flags", 0)
            
            print(
                f"\n=== КОРАБЛЬ ===\n"
                f"Название: {state.ship_name}\n"
                f"Система: {state.current_system}\n"
                f"Топливо: {state.fuel:.1f} T\n"
                f"Энергия: SYS[{state.pips[0]}] ENG[{state.pips[1]}] WEP[{state.pips[2]}]\n"
                f"Груз: {state.total_cargo} T\n"
                f"Прочность: {state.health:.1f}%\n"
                f"Опасность: {'Да' if state.in_danger else 'Нет'}\n"
                f"Цель захвачена: {'Да' if state.target_locked else 'Нет'}\n"
                f"Режим: {EliteIntegration.parse_ship_mode(flags)}\n"
            )
            time.sleep(5)
            
    except KeyboardInterrupt:
        integrator.stop()
        print("\nМониторинг остановлен.")

if __name__ == "__main__":
    main()