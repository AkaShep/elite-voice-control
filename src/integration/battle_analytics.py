# src/integration/battle_analytics.py Шаблон для умной аналитики боя

def generate_battle_report(ctx):
    stats = ctx.battle_stats
    summary = []
    summary.append(f"Бой завершён.")
    summary.append(f"Получено урона: {stats['damage_taken']:.1f}%.")
    if stats['enemies']:
        summary.append(f"Противники: {', '.join(stats['enemies'])}.")
    if stats['consumables']:
        summary.append(f"Использовано расходников: {', '.join(stats['consumables'])}.")
    if stats['shots_fired']:
        summary.append(f"Выстрелов произведено: {stats['shots_fired']}.")
    if stats['enemy_actions']:
        summary.append(f"Противник атаковал {len(stats['enemy_actions'])} раз.")
    if stats['hull_damage_events']:
        severe = [e for e in stats['hull_damage_events'] if e.Health and e.Health < 50]
        if severe:
            summary.append(f"Внимание: {len(severe)} раза броня опускалась ниже 50 процентов.")
    # Добавляй сюда любые дополнительные показатели!
    return " ".join(summary)
