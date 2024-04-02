"""
Описан класс, представляющий бюджет
"""
from dataclasses import dataclass
from datetime import timedelta


@dataclass(slots=True)
class Budget():
    """
    Бюджет>.
    plan - величина запланированных расходов
    duration - длительность промежутка подсчетов, отсчитывается назад от текущего момента времени
    """
    plan: float = 0
    duration: timedelta = "0 days"
    pk: int | None = None
