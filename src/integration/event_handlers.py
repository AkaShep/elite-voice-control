# Обработчики событий
from voice.tts.tts_engine import TtsEngine
from .context import GameContext
from .battle_analytics import generate_battle_report

tts = TtsEngine()
ctx = GameContext()
mode_manager = None  # подключим из integration.py

# --- Новое: обработчики голосовых команд
def handle_routine_command(cmd):
    if cmd == "открой карту":
        tts.synthesize("Открываю карту галактики.")
    elif cmd == "боевой режим":
        if mode_manager:
            mode_manager.start_combat_mode()
        tts.synthesize("Перехожу в боевой режим.")
    elif cmd == "выход":
        tts.synthesize("Ассистент завершает работу.")
        exit(0)
    else:
        tts.synthesize(f"Команда не распознана: {cmd}")

def handle_combat_command(cmd):
    if cmd == "ракеты":
        tts.synthesize("Пуск ракет.")
    elif cmd == "щит":
        tts.synthesize("Активирую щит.")
    elif cmd == "отступить":
        tts.synthesize("Экстренное отступление!")
    elif cmd == "выход из боя":
        ctx.end_battle("manual")
        if mode_manager:
            mode_manager.start_routine_mode()
        tts.synthesize("Бой завершён. Возвращаюсь к обычным командам.")
    else:
        tts.synthesize(f"Неизвестная команда: {cmd}")

def handle_location(event):
    ctx.enter_system(event.StarSystem)
    # Пример расширенной логики (можно добавить фразу по известным системам)
    if event.StarSystem == "Sol":
        tts.synthesize("Добро пожаловать в систему Сол. Внимание: территория Федерации.")
    else:
        tts.synthesize(f"Вход в систему {event.StarSystem}")

def handle_routine_command(command):
    if command == "открой карту":
        tts.synthesize("Открываю карту галактики.")        

def handle_fsd_jump(event):
    ctx.enter_system(event.StarSystem)
    tts.synthesize(f"Гиперпрыжок завершён. Вход в систему {event.StarSystem}")

def handle_targeted(event):
    if not ctx.battle_mode and event.TargetLocked:
        ctx.start_battle(event.timestamp)
        enemy = event.PilotName or event.Ship or "противник"
        ctx.register_enemy(enemy)
        tts.synthesize(f"Вас взяли в прицел. Перехожу в боевой режим. Противник: {enemy}")
    elif ctx.battle_mode and not event.TargetLocked:
        ctx.end_battle(event.timestamp)
        summary = ctx.get_battle_summary()
        tts.synthesize(
            f"Бой завершён. Урон: {summary['dmg']}. Противники: {summary['enemies']}. "
            + (f"Продолжительность боя: {summary['duration']} секунд." if summary['duration'] else "")
        )

def handle_hull_damage(event):
    if ctx.battle_mode:
        ctx.register_hull_damage(event)
        if event.Health is not None and event.Health < 80:
            tts.synthesize("Внимание, повреждение корпуса! Рекомендую отступить.")

def handle_battle_end(event):
    if ctx.battle_mode:
        ctx.end_battle(event.timestamp)
        summary = ctx.get_battle_summary()
        tts.synthesize(
            f"Бой завершён. Урон: {summary['dmg']}. Противники: {summary['enemies']}. "
            + (f"Продолжительность боя: {summary['duration']} секунд." if summary['duration'] else "")
        )
