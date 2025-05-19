# src/integration/context.py Хранит всё состояние игры
class GameContext:
    def __init__(self):
        self.current_system = None
        self.battle_mode = False
        self.assistant_mode = "routine"  # 'routine' или 'combat'
        self.battle_stats = {}
        self.reset_battle_stats()

    def reset_battle_stats(self):
        self.battle_stats = {
            "damage_taken": 0.0,
            "enemies": set(),
            "consumables": [],
            "shots_fired": 0,
            "hull_damage_events": [],
            "enemy_actions": [],
            "battle_started_at": None,
            "battle_ended_at": None,
        }

    def enter_system(self, system_name):
        self.current_system = system_name
        self.battle_mode = False
        self.assistant_mode = "routine"
        self.reset_battle_stats()

    def start_battle(self, timestamp):
        self.battle_mode = True
        self.assistant_mode = "combat"
        self.battle_stats["battle_started_at"] = timestamp

    def register_enemy(self, enemy_name):
        if enemy_name:
            self.battle_stats["enemies"].add(enemy_name)

    def register_hull_damage(self, event):
        self.battle_stats["hull_damage_events"].append(event)
        self.battle_stats["damage_taken"] += event.Health or 0

    def use_consumable(self, name):
        self.battle_stats["consumables"].append(name)

    def register_shot(self):
        self.battle_stats["shots_fired"] += 1

    def register_enemy_action(self, event):
        self.battle_stats["enemy_actions"].append(event)

    def end_battle(self, timestamp):
        self.battle_mode = False
        self.assistant_mode = "routine"
        self.battle_stats["battle_ended_at"] = timestamp

    def get_battle_summary(self):
        from datetime import datetime
        stats = self.battle_stats
        duration = None
        if stats["battle_started_at"] and stats["battle_ended_at"]:
            fmt = "%Y-%m-%dT%H:%M:%SZ"
            dt1 = datetime.strptime(stats["battle_started_at"], fmt)
            dt2 = datetime.strptime(stats["battle_ended_at"], fmt)
            duration = int((dt2 - dt1).total_seconds())
        summary = f"Бой завершён. Урон: {stats['damage_taken']:.1f}. "
        summary += f"Противники: {', '.join(stats['enemies']) or 'не обнаружены'}. "
        if stats['consumables']:
            summary += f"Использовано расходников: {', '.join(stats['consumables'])}. "
        if stats['enemy_actions']:
            summary += f"Враг атаковал {len(stats['enemy_actions'])} раз. "
        if duration:
            summary += f"Длительность: {duration} сек."
        return summary
