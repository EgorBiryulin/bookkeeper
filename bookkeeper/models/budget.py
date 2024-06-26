# Описан класс, представляющий бюджет

from dataclasses import dataclass
from datetime import timedelta


@dataclass(slots=True)
class Budget:

    # Модель бюджетного ограничения.

    # Параметры модели:
    # plan - величина запланированных расходов;
    # duration - длительность промежутка подсчетов,
    # отсчитывается назад от текущего момента времени.

    duration: timedelta
    plan: float = 1000
