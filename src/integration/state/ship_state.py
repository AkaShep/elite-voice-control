# текущее состояние корабля
class ShipState:
    def __init__(self):
        self.current_system = "Unknown"
        self.jump_count = 0

    def on_fsd_jump(self, event):
        self.current_system = event.StarSystem
        self.jump_count += 1
        print(f"Jumped to {self.current_system} (#{self.jump_count})")
