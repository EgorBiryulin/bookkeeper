"""
Описан класс, представляющий расходную операцию
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Expense:
    """
    Расходная операция.
    pk - id записи в базе данных
    added_date - дата добавления в бд
    expense_date - дата расхода
    category - id категории расходов
    amount - сумма
    comment - комментарий
    """
    pk: int
    added_date: str
    expense_date: str
    category: str
    amount: float
    comment: str

