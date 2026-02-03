"""
Regras de gamificação: ex. se nota > 80 = medalha ouro, XP, nível.
"""
from typing import Literal

BRONZE_THRESHOLD = 60
SILVER_THRESHOLD = 80
GOLD_THRESHOLD = 90

XP_PER_BRONZE = 10
XP_PER_SILVER = 25
XP_PER_GOLD = 50


def badge_for_grade(grade_percent: float) -> Literal["gold", "silver", "bronze"] | None:
    """Retorna tipo de medalha conforme a nota (0–100)."""
    if grade_percent >= GOLD_THRESHOLD:
        return "gold"
    if grade_percent >= SILVER_THRESHOLD:
        return "silver"
    if grade_percent >= BRONZE_THRESHOLD:
        return "bronze"
    return None


def xp_for_badge(badge: str) -> int:
    """XP concedido por tipo de medalha."""
    return {"gold": XP_PER_GOLD, "silver": XP_PER_SILVER, "bronze": XP_PER_BRONZE}.get(
        badge, 0
    )


def level_from_total_xp(total_xp: int) -> int:
    """Calcula nível a partir do XP total (ex: 100 XP por nível)."""
    xp_per_level = 100
    return max(1, (total_xp // xp_per_level) + 1)
