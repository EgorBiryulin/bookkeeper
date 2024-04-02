"""
Описан класс, представляющий расходную операцию
"""

from dataclasses import dataclass, field
from datetime import datetime


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

    amount: int = 0
    category: int = 0
    #expense_date: datetime = field(default_factory=datetime.now)
    added_date: datetime = field(default_factory=datetime.now)
    comment: str = ''
    pk: int = 0

    #def __init__(self, expense_date: str, category: str, amount: float, comment: str):
    #    self.expense_date = expense_date
    #    self.category = category
    #    self.amount = amount
    #    self.comment = comment
    #    self.pk: int
