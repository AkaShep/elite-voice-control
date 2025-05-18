import logging
from events import EventTypes

class ShipState:
    def __init__(self):
        self.fuel = 0.0
        self.health = 100.0
        self.pips = [0, 0, 0]  # 0-4 (ENG, WEP, SYS)
        self.ship_name = ""
        self.cargo = []
        self.total_cargo = 0
        self._update_callbacks = []
        self.current_system = ""
        self.in_danger = False
        self.target_locked = False

    def add_callback(self, callback):
        """Подписка на изменения состояния"""
        self._update_callbacks.append(callback)  

    def _notify_callbacks(self):
        """Уведомление подписчиков"""
        for callback in self._update_callbacks:
            callback(self)

    def update_from_status(self, status: dict):
        try:
            # Обновление основных параметров
            raw_pips = status.get("Pips", [0, 0, 0])
            self.pips = [p // 2 for p in raw_pips]
            self.fuel = status.get("Fuel", {}).get("FuelMain", 0.0)
            self.health = max(0.0, min(status.get("HullHealth", 1.0) * 100, 100.0))
            self.total_cargo = int(status.get("Cargo", 0))
            self._notify_callbacks()
            
        except KeyError as e:
            logging.warning(f"Missing key in status: {str(e)}")
        except Exception as e:
            logging.error(f"Status update error: {str(e)}", exc_info=True)    
        
    def update_from_journal_event(self, event: dict):
        event_type = event.get("event")
        try:
            if event_type == EventTypes.LOADOUT:
                self.ship_name = event.get("Ship", "Unknown")
                logging.info(f"Ship updated: {self.ship_name}")
                
            elif event_type == EventTypes.FUEL_SCOOP:
                scooped = event.get("Scooped", 0.0)
                self.fuel += scooped
                logging.info(f"Fuel scooped: +{scooped} tons")
                
            elif event_type == EventTypes.UNDER_ATTACK:
                self.in_danger = True
                logging.warning("Under attack!")
                
            elif event_type == EventTypes.CARGO:
                self.cargo = event.get("Inventory", [])
                self.total_cargo = len(self.cargo)
                
            self._notify_callbacks()
            
        except Exception as e:
            logging.error(f"Journal update error: {str(e)}", exc_info=True)